from tempfile import TemporaryFile
from flask import Flask, render_template
from flask_cors import CORS

from mc2 import DataParser

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])


@app.route("/data", methods=["GET"])
def get_data():
    parser = DataParser()
    data = parser.parse("mc2.txt")
    return data

@app.route("/counts",methods=["GET"])
def get_counts():
    parser = DataParser()
    counts = parser.student_counts("mc2.txt")
    return counts

@app.route("/", methods=["GET","POST"])
def hello():
    render_template("index.html")

if __name__ == "__main__":
    app.run(port=5001)