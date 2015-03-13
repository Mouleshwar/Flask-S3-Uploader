from flask import Flask, render_template, flash
from flask_wtf import Form
from flask_wtf.file import FileField
from tools import s3_upload
import json 

app = Flask(__name__)
app.config.from_object('config')


class UploadForm(Form):
    example = FileField('Example File')


@app.route('/', methods=['POST', 'GET'])
def upload_page():
    form = UploadForm(csrf_enabled=False)
    if form.validate_on_submit():
        output = s3_upload(form.example)
        flash('{src} uploaded to S3 as {dst} and its urs is {url}'.format(src=form.example.data.filename, dst=output.split(" ")[0], url=output.split(" ")[1]))
        response = {}
        response['url'] = output.split(" ")[1]
        return json.dumps(response, indent=4)
    return render_template('example.html', form=form)    

if __name__ == '__main__':
    app.run()
