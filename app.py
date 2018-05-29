import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc,select

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################
from flask_sqlalchemy import SQLAlchemy

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Belly_Button_BiodiversityHW/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)

class Emoji(db.Model):
    __tablename__ = 'emoji'

    otu_id = db.Column(db.Integer, primary_key=True)
    lowest_taxonomic_unit_found = db.Column(db.String)


    def __repr__(self):
        return '<Emoji %r>' % (self.name)

# Create database tables
@app.before_first_request
def setup():
    # Recreate database each time for demo
    # db.drop_all()
    db.create_all()

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/names")
def emoji_char_data():
    """Return a list of sample names in the format"""

    # query for the top 10 emoji data
    results = db.session.query(samples).\
        order_by(Emoji.score.desc()).\
        limit(10).all()

    # Select the top 10 query results
    emoji_char = [result[0] for result in results]
    scores = [int(result[1]) for result in results]

    # Generate the plot trace
    plot_trace = {
        "x": emoji_char,
        "y": scores,
        "type": "bar"
    }
    return jsonify(plot_trace)



@app.route("/otu")
def otu():
    """Return list of OTU descriptions"""

    # query for the emoji data using pandas
    query_statement = db.session.query(Emoji).\
    order_by(Emoji.score.desc()).\
    limit(10).statement
    df = pd.read_sql_query(query_statement, db.session.bind)

    # Format the data for Plotly
    plot_trace = {
            "x": df["emoji_id"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

@app.route("/emoji_name")
def emoji_name_data():
    """Return emoji score and emoji name"""

    # query for the top 10 emoji data
    results = db.session.query(Emoji.name, Emoji.score).\
        order_by(Emoji.score.desc()).\
        limit(10).all()
    df = pd.DataFrame(results, columns=['name', 'score'])

    # Format the data for Plotly
    plot_trace = {
            "x": df["name"].values.tolist(),
            "y": df["score"].values.tolist(),
            "type": "bar"
    }
    return jsonify(plot_trace)

if __name__ == '__main__':
    app.run(debug=True)
