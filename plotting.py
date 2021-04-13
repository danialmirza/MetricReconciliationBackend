import bokeh
from bokeh.plotting import Figure
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import column
from bokeh.models import CustomJS, ColumnDataSource, Slider
from bokeh.sampledata.autompg import autompg

from numpy import cos, linspace

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