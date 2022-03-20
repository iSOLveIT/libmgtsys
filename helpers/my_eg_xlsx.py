from openpyxl import Workbook, load_workbook
from tempfile import NamedTemporaryFile
import os
import re
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UPLOAD_FOLDER'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000


def allowed_file(filename):
    pattern = r"^[\w\-]+?.(xlsx)$"
    check_file = re.search(pattern, filename)
    return '.' in filename and check_file is not None


def process_data(header, file_data):
    sorted(list(set(file_data)), key=lambda x: x[4])
    return dict(tbl_head=header, tbl_content=sorted(list(set(file_data)), key=lambda x: x[4]))


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            wb = load_workbook(file)

            with NamedTemporaryFile() as tmp:
                wb.save(tmp.name)   # Save file in temporary file
                tmp.seek(0)

                wb2 = load_workbook(tmp)
                ws = wb2.active
                # TODO: Remove the first row as header from the list of rows
                #  then send it as a parameter with the new list
                get_data = list(tuple(ws.iter_rows(max_col=6, min_row=1, values_only=True)))
                data_header = get_data.pop(0)
                content = process_data(data_header, get_data)

            return render_template("upload_file.html", content=content)

    return render_template("upload_file.html")


if __name__ == '__main__':
    app.run()
