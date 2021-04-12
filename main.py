
import json
import urllib
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS

import bokeh
from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.sampledata.autompg import autompg

from numpy import cos, linspace

app = Flask(__name__)
CORS(app)
DB_URI = "mongodb+srv://admin:" + urllib.parse.quote(<password>) + "@cluster0.872hs.mongodb.net/test"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField(required=True)
    password = db.StringField(required=True)

    def to_json(self):
        return {"name": self.name,
                "password": self.password}

class Metric(db.Document):
    reporter = db.ReferenceField(User)
    metricName = db.StringField(required=True)
    database = db.StringField(required=True, choices=('NDW', 'MELD'))
    schema = db.StringField(required=True)
    table = db.StringField(required=True)
    metricId = db.StringField(required=True)
    metricCol = db.StringField(required=True)
    exclusions = db.DictField()
    geos = db.DictField()
    timeCol = db.StringField()
    timeDensity = db.StringField(choices=(('D', 'Day'), ('W', 'Week'), ('M', 'Month'), ('Y', 'Year'), ('DW', 'DayOfWeek')))
    dateRange = db.DictField()


@app.route('/create', methods=['PUT'])
def create_record():
    record = json.loads(request.data)
    user = User(name=record['name'],
                password=record['password'])

    user.save()
    return jsonify(user.to_json())

@app.route('/login', methods=['POST'])
def get_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name'],
                        password=record['password']).first()

    if not user:
        return jsonify({'error': 'user not found',
                        'auth': False})
    else:
        return jsonify({'auth': True})

@app.route('/report', methods=['PUT'])
def create_metric():
    record = json.loads(request.data)
    metric = Metric(reporter=record['reporter'],
                    metricName=record['metricName'],
                    database=record['database'],
                    schema=record['schema'],
                    table=record['table'],
                    metricId=record['metricId'],
                    metricCol=record['metricCol'],
                    exclusions=record['exclusions'],
                    geos=record['geos'],
                    timeCol=record['timeCol'],
                    timeDensity=record['timeDensity'],
                    dateRange=record['dateRange'])

    metric.save()
    return jsonify(metric.to_json())

@app.route('/query', methods=['POST'])
def query_metric():
    record = json.loads(request.data)
    metric1 = Metric.objects(metricName=record['metricName1'],
                            table=record['table1']).first()
    metric2 = Metric.objects(metricName=record['metricName2'],
                            table=record['table2']).first()

    if not (metric1 and metric2):
        return jsonify({'error': 'metric not defined',
                        'status': False})
    else:
        return jsonify({'status': True,
                        'metadata1': metric1,
                        'metadata2': metric2,
                        'plot': plot1()})

def plot1():
    # copy/pasted from Bokeh Getting Started Guide
    x = linspace(-6, 6, 100)
    y = cos(x)
    p = Figure(width=500, height=500, toolbar_location="below",
               title="Plot 1")
    p.circle(x, y, size=7, color="firebrick", alpha=0.5)

    # following above points:
    #  + pass plot object 'p' into json_item
    #  + wrap the result in json.dumps and return to frontend
    return bokeh.embed.json_item(p, "myplot")

if __name__ == "__main__":
    app.run(debug=True)
