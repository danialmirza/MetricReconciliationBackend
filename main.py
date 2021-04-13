
import json
import urllib
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask_cors import CORS

from plotting import plot_metric_by_day, metric_comparison
import pandas as pd
app = Flask(__name__)
CORS(app)

#f = open("mongo-uri.txt", "r")
#mongoURI = f.readline()[0]
app.config["MONGODB_HOST"] = "mongodb+srv://admin:" + urllib.parse.quote('[P@ssw0rd]') + "@cluster0.872hs.mongodb.net/test"

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
    source = db.StringField(required=True)
    description = db.StringField(required=True)
    organisation = db.StringField(required=True)
    database = db.StringField(required=True, choices=('NDW', 'MELD'))
    schema = db.StringField(required=True)
    table = db.StringField(required=True)
    metricId = db.StringField(required=True)
    metricCol = db.StringField(required=True)
    metricNumer = db.StringField(required=True)
    metricDenom = db.StringField()
    exclusions = db.DictField()
    geos = db.DictField()
    divisionCol = db.StringField()
    regionCol = db.StringField()
    topGeoAgg = db.StringField(required=True, choices=('ENT', 'NED', 'WES', 'CEN', 'Other'))
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
                    source=record['source'],
                    description=record['description'],
                    organisation=record['organisation'],
                    database=record['database'],
                    schema=record['schema'],
                    table=record['table'],
                    metricId=record['metricId'],
                    metricCol=record['metricCol'],
                    metricNumer=record['metricNumer'],
                    metricDenom=record['metricDenom'],
                    exclusions=record['exclusions'],
                    geos=record['geos'],
                    divisionCol=record['divisionCol'],
                    regionCol=record['regionCol'],
                    topGeoAgg=record['topGeoAgg'],
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
        df1 = pd.read_csv('sample_data/attr_metrics_mart_202103.csv')
        df2 = pd.read_csv('sample_data/attr_all_west_202103.csv')
        return jsonify({'status': True,
                        'metadata1': metric1,
                        'metadata2': metric2,
                        'metricTable': metric_comparison(metric1, metric2),
                        'plot': plot_metric_by_day('Average Time to Repair', df1, metric1.metricName,
                                                   metric1.metricNumer, metric1.metricDenom,
                                                   metric1.timeCol, df2, metric2.metricName,
                                                   metric2.metricNumer, metric2.metricDenom,
                                                   metric2.timeCol, metric1.topGeoAgg, metric2.topGeoAgg)})

if __name__ == "__main__":
    app.run(debug=True)
