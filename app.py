from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import ingest_data, get_from_mongo

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
@cross_origin()
def home_page():
    return render_template("index.html")


@app.route("/scrap", methods=["POST", "GET"])
def retrieve_data():
    if request.method == "POST":
        message = ingest_data.insert_data()
        return render_template("data_inserted.html", message=message)


@app.route("/courses", methods=["POST", "GET"])
def display_courses():
    if request.method == "POST":
        content = get_from_mongo.get_from_mongo()
        return render_template("result.html", content=content)


if __name__ == "__main__":
    app.run(debug=True)

