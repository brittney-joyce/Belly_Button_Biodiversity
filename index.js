function sample_names() {
  var select = document.getElementById("sample-metadata");
  var url = "/names"

  Plotly.d3.json(url, function(error, response) {
    if (error) return console.warn(error);
    var data = response;
    data.map(function(sample){
        var option = document.createElement('option')
        option.text = sample
        option.value = sample
        selector.appendChild(option)
      });
    });
};
#################################################
# Create Bubble Chart
#################################################
var bubble_chart = {
  margin: { t: 0 },
  xaxis: { title: 'OTU ID' }
};

var bubble_data =[{
  x: sampleData[0]['otu_ids'],
  y: sampleData[0]['sample_values'],
  text: labels,
  mode: 'markers',
  marker: {
    size: sampleData[0]['sample_values'],
    color: sampleData[0]['otu_ids'],
}];
var bubble = document.getElementById('bubble');
Plotly.plot(bubble,bubble_chart, bubble_data);

#################################################
# Create Pie Chart
#################################################
var pieData = [{
    values: sampleData[0]['sample_values'].slice(0, 10),
    labels: sampleData[0]['otu_ids'].slice(0, 10),
    hovertext: labels.slice(0, 10),
    hoverinfo: 'hovertext',
    type: 'pie'

var pie = document.getElementById('pie');
Plotly.plot(pie, pieData);

function updateCharts(sampleData, otuData) {
    var sampleValues = sampleData[0]['sample_values'];
    var otuIDs = sampleData[0]['otu_ids'];
