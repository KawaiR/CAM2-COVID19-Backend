import flask
import matplotlib.pyplot as plt
import numpy as np
from flask import send_file, render_template
import os

PIC_FOLDER = os.path.join('static', 'some_photo')

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = PIC_FOLDER

@app.route('/plot-test')
def generate_graph():
  arr = np.array([[2,2,5,5], [5,5,2,2], [4,4,3,3],[3,3,4,4]])
  plt.pcolor(arr, cmap=plt.cm.BuPu)
  plt.colorbar(orientation='vertical')
  plt.axis('image')
  plt.savefig('Graph.png')

  file_name = os.path.join(app.config['UPLOAD_FOLDER'], 'Graph.png')
  
  return render_template("plot-test.html", user_image=file_name)
  
@app.route('/')
def index():
  return "<h1>CAM2-COVID19 Backend</h1><p> Hello, World!</p>"

if __name__ == '__main__':
  app.run(debug=True)
