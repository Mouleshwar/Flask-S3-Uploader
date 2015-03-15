from flask import Flask, render_template, flash
from flask_wtf import Form
from flask_wtf.file import FileField
from tools import s3_upload, store_locally
import json 

app = Flask(__name__)
app.config.from_object('config')


class UploadForm(Form):
    example = FileField('Example File')


@app.route('/', methods=['POST', 'GET'])
def upload_page():
    form = UploadForm(csrf_enabled=False)
    upload_file = form.example
    if form.validate_on_submit():
        output = store_locally(upload_file)
        response = {}
        if output is not None:
            response['url'] = output
            return json.dumps(response, indent=4)
        else:
            response['url'] = None
            return json.dumps(response, indent=4), app.config["INVALID_DATA"] 
    return render_template('example.html', form=form)    

if __name__ == '__main__':
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])
