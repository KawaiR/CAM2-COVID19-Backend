import flask
import matplotlib.pyplot as plt
plt.ioff()
import numpy as np
from flask import send_file, render_template, request, json
import os
import mpld3
from mpld3 import plugins
import json


def plot(start, end):
  x = range(start, end)
  y = range(start, end)
  fig, ax = plt.subplots()
  ax.plot(x, y)
  fig.set_size_inches(2, 1.5)
  return mpld3.fig_to_html(fig)


PIC_FOLDER = os.path.join('static', 'some_photo')

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = PIC_FOLDER


@app.route('/')
def index():
  return render_template("index.html")

@app.route('/query', methods = ['POST'])
def query():
  data = json.loads(request.data)
  plt_html = plot(data["start"], data["end"])
  # print(plt_html)
  return plt_html

"""
@app.route('/plot-test')
def generate_graph():
  arr = np.array([[2,2,5,5], [5,5,2,2], [4,4,3,3],[3,3,4,4]])
  plt.pcolor(arr, cmap=plt.cm.BuPu)
  plt.colorbar(orientation='vertical')
  plt.axis('image')
  plt.savefig('Graph.png')

  file_name = os.path.join(app.config['UPLOAD_FOLDER'], 'Graph.png')
  
  return render_template("plot-test.html", user_image=file_name)
"""

if __name__ == '__main__':
  app.run(debug=True)
