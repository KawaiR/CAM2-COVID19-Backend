import flask
import matplotlib.pyplot as plt
plt.ioff()
import numpy as np
from flask import send_file, render_template, request, json
import os
import mpld3
from mpld3 import plugins
import json
import random

# This function generates the plot
def plot(start, end):
  x = range(start, end)
  y = range(start, end)
  fig, ax = plt.subplots()
  ax.scatter(x, y)
  ax.set(title="Vehicle count from date " + str(start) + " to " + str(end))
  fig.set_size_inches(2, 1.5)
  return mpld3.fig_to_html(fig)


app = flask.Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

# This function get the POST request and return the plot in format of html
@app.route('/query', methods = ['POST'])
def query():
  # Get data from ajax request
  data = json.loads(request.data)
  plt_html = plot(int(data["start"]), int(data["end"]))
  return plt_html


if __name__ == '__main__':
  app.run(debug=True)
