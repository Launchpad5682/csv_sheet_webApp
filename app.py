import os
from flask import (
    Flask,
    flash,
    request,
    redirect,
    url_for,
    send_from_directory,
    render_template,
)
import pandas as pd

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = (
    "/home/launchpad5682/projects/arth-ws/arth-technologies/csv_sheets_webApp/tmpFiles/"
)
ALLOWED_EXTENSIONS = {"csv"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect(url_for("visualize_file", filename=filename))
    return render_template("upload_form.html")


@app.route("/visualize/<filename>")
def visualize_file(filename):
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    dataframe = pd.read_csv(path)
    columnsList = list(dataframe.columns.values)
    print(columnsList)
    print(type(columnsList[0]))
    dataList = list(dataframe.values)
    return render_template("table.html", dataList=dataList,columnsList=columnsList)

@app.route("/edit")
def update_sheet():
    return 'Hello World'

# Download the updated file
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


app.run(port=5555, debug=True)
