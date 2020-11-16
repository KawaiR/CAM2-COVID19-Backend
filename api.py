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
import scatterplots
from datetime import date


# This function generates the plot
def plot(country, state, start, end):
  if country == "United States":
    return scatterplots.generate_plot(state=state, date1=start, date2=end)
  else:
    return scatterplots.generate_plot(country=country, date1=start, date2=end)


app = flask.Flask(__name__)

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/analysis/')
def analysis():
  today = date.today()
  max_date = today.strftime("%Y-%m-%d")
  min_date = "2020-04-01"
  return render_template("analysis.html", min_date=min_date, max_date=max_date)

@app.route('/research/')
def research():
  return render_template("research.html")

@app.route('/members/')
def members():
  return render_template("members.html")

@app.route('/timeline/')
def timeline():
  return render_template("timeline.html")

# This function get the POST request and return the plot in format of html
@app.route('/query', methods = ['POST'])
def query():
  # Get data from ajax request
  data = json.loads(request.data)
  scatter, hist = plot(data["country"], data["state"], data["start"], data["end"])
  data = {}
  data['scatter'] = scatter
  data['hist'] = hist
  json_data = json.dumps(data)
  return json_data


if __name__ == '__main__':
  app.run(debug=True)
