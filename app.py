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
engine = create_engine ("sqlite:///Belly_Button_BiodiversityHW/belly_button_biodiversity.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


OTU = Base.classes.otu
Samples = Base.classes.samples
Samples_Metadata= Base.classes.samples_metadata


session = Session(engine)

#################################################
# Flask Routes
#################################################

# Create database tables
@app.before_first_request
def setup():
    db.create_all()

@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html")

@app.route("/names")
def names():
    """Return a list of sample names in the format"""

    # query for the top 10 emoji data
    results = db.session.query(samples).statement
    df = pd.read_sql_query(stmt, session.bind)
    df.set_index('otu_id', inplace=True)

    return jsonify(list(df.columns))


@app.route("/otu")
def otu():
    """Return list of OTU descriptions"""
    results = session.query(OTU.lowest_taxonomic_unit_found).all()

otu_list = list(np.ravel(results))
    return jsonify(otu_list)


@app.route("/samples_metadata")
def sample_metadata(sample):

    sel = [Samples_Metadata.SAMPLEID, Samples_Metadata.ETHNICITY,
           Samples_Metadata.GENDER, Samples_Metadata.AGE,
           Samples_Metadata.LOCATION, Samples_Metadata.BBTYPE]


if __name__ == '__main__':
    app.run(debug=True)
