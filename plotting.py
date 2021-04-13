import bokeh
from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider, Div, RangeSlider, DateRangeSlider, Spinner
from bokeh.sampledata.autompg import autompg
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, HTMLTemplateFormatter

from numpy import cos, linspace
import pandas as pd

def metric_comparison(metric1, metric2):
    print(metric1.metricName)
    print(metric2)
    data = {
        'Field':['Metric Name', 'Source', 'Organisation', 'Database',
               'Schema', 'Table', 'Metric Numerator', 'Metric Denominator',
               'Exclude Bulk?', 'Residential Only?', 'Exclude Courtesy?',
               'Exclude IE?', 'Exclude Prepaid?', 'Geography', 'Time granularity',
               'Start Date', 'End Date'],
        'Metric1':[metric1.metricName, metric1.source,
                 metric1.organisation, metric1.database, metric1.schema,
                 metric1.table, metric1.metricNumer, metric1.metricDenom,
                 metric1.exclusions['excl_bulk'], metric1.exclusions['excl_resi'],
                 metric1.exclusions['excl_courtesy'], metric1.exclusions['excl_ie'],
                 metric1.exclusions['excl_prepaid'], metric1.topGeoAgg, metric1.timeDensity,
                 metric1.dateRange['start_date'], metric1.dateRange['end_date']],
        'Metric2':[metric2.metricName, metric2.source,
                 metric2.organisation, metric2.database, metric2.schema,
                 metric2.table, metric2.metricNumer, metric2.metricDenom,
                 metric2.exclusions['excl_bulk'], metric2.exclusions['excl_resi'],
                 metric2.exclusions['excl_courtesy'], metric2.exclusions['excl_ie'],
                 metric2.exclusions['excl_prepaid'], metric2.topGeoAgg, metric2.timeDensity,
                 metric2.dateRange['start_date'], metric2.dateRange['end_date']]
    }

    source = ColumnDataSource(data)

    template = """
                <div style="background:<%= 
                    (function colorfromint(){
                        if(Metric1 != Metric2 ){
                            return("yellow")}
                        }()) %>; 
                    color: <%= 
                        (function colorfromint(){
                            if(Metric1 != Metric2){return('red')}
                            }()) %>;"> 
                    <%= value %>
                    </font>
                </div>
                """
    formatter = HTMLTemplateFormatter(template=template)

    columns = [
        TableColumn(field="Field", title="Field"),
        TableColumn(field="Metric1", title="Metric 1"),
        TableColumn(field="Metric2", title="Metric 2", formatter=formatter)
    ]
    data_table = DataTable(source=source, columns=columns, width=800, height=500)
    return bokeh.embed.json_item(data_table, "mytable")


def plot_metric_by_day(fig_title, df1, metric1_name, num1, denom1, dt1, df2, metric2_name, num2, denom2, dt2, div1=None,
                       div2=None):
    color_dict = {
        'ENT': (43, 156, 216),
        'WES': (51, 153, 51),
        'NED': (100, 77, 160),
        'CEN': (254, 84, 11)
    }
    if denom1 and denom2:
        df1 = df1.copy()

        df1 = df1.groupby(dt1)[[num1, denom1]].sum().reset_index()
        df1['dt'] = pd.to_datetime(df1[dt1])

        df2 = df2.copy()

        df2 = df2.groupby(dt2)[[num2, denom2]].sum().reset_index()
        df2['dt'] = pd.to_datetime(df2[dt2])

        df1['value'] = df1[num1] / df1[denom1]
        df2['value'] = df2[num2] / df2[denom2]
    else:
        df1 = df1.copy()
        df1 = df1.groupby(dt1)[[num1]].sum().reset_index()
        df1['dt'] = pd.to_datetime(df1[dt1])

        df2 = df2.copy()
        df2 = df2.groupby(dt2)[[num2]].sum().reset_index()
        df2['dt'] = pd.to_datetime(df2[dt2])

        df1['value'] = df1[num1]
        df2['value'] = df2[num2]

    if div1 == div2 and div1 is not None:
        line1_dash = 'dashed'
        line2_dash = 'dotted'
    else:
        line1_dash = 'solid'
        line2_dash = 'solid'

    if div1 in ['NED', 'CEN', 'WES', 'ENT']:
        r, g, b = color_dict[div1]
        color_1 = bokeh.colors.RGB(r, g, b)
    else:
        color_1 = 'blue'

    if div2 in ['NED', 'CEN', 'WES', 'ENT']:
        r, g, b = color_dict[div2]
        color_2 = bokeh.colors.RGB(r, g, b)
    else:
        if color_1 == 'blue':
            color_2 = 'red'
        if color_1 == 'red':
            color_2 = 'blue'

    p = Figure(title=fig_title, x_axis_type='datetime')
    p.line(df1['dt'], df1['value'], line_width=2, line_color=color_1, legend_label=metric1_name, line_dash=line1_dash)
    p.line(df2['dt'], df2['value'], line_width=2, line_color=color_2, legend_label=metric2_name, line_dash=line2_dash)

    return bokeh.embed.json_item(p, "plot")

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