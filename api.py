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
def plot(place, start, end):
  return scatterplots.generate_plot(country=place, date1=start, date2=end)


app = flask.Flask(__name__)

@app.route('/analysis')
def analysis():
  today = date.today()
  max_date = today.strftime("%Y-%m-%d")
  min_date = "2020-04-01"
  countries = ["United States", "Australia", "France",
                     "Austria", "Denmark", "Great Britain",
                     "Czech Republic", "Switzerland", "Italy",
                     "Germany", "Canada", "New Zealand",
                     "Hong Kong", "Spain", "Hungary"]
  return render_template("analysis.html", min_date=min_date, max_date=max_date, countries=countries)

@app.route('/research')
def research():
  return render_template("research.html")

@app.route('/members')
def members():
  return render_template("members.html")

@app.route('/timeline')
def timeline():
  return render_template("timeline.html")

# This function get the POST request and return the plot in format of html
@app.route('/query', methods = ['POST'])
def query():
  # Get data from ajax request
  data = json.loads(request.data)
  plt_html = plot(data["country"], data["start"], data["end"])
  return plt_html


if __name__ == '__main__':
  app.run(debug=True)
