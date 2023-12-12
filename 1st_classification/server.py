# Copyright 2023 Ar-Ray-code
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from modules.zip_interface import ZipInterface
import flask
from flask import request, send_file

form_html = """
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>1st_classification</title>
    </head>
    <body>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="zip">
            <input type="submit">
            <br>
            <label for="prompt_text">Prompt Text:</label>
            <input type="text" name="prompt_text" id="prompt_text" value="a photography of">
            <br>
            <label for="target_keywords">Target Keywords (comma-separated):</label>
            <input type="text" name="target_keywords" id="target_keywords" value="person,cat,dog">
            <br>
        </form>
    </body>
</html>
"""

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['POST'])
def load():
    zip_interface = ZipInterface()
    input_bin = request.files['zip'].read()
    print('--input_bin--')
    print('input_bin-size: ', len(input_bin))
    # if over 100MB, return error
    if len(input_bin) > 100000000:
        return 'File size is too large. Please upload a file smaller than 100MB.'

    prompt_text = request.form['prompt_text']
    if prompt_text == '':
        prompt_text = 'a photography of'
    target_keywords = request.form['target_keywords'].split(',')
    target_keywords = [x.strip() for x in target_keywords]
    zip_interface.load(upload_zip_binary=input_bin,
                       prompt_text=prompt_text,
                       target_keywords=target_keywords)
    result_filename = zip_interface.run()
    del zip_interface
    return send_file(result_filename, mimetype='application/zip', download_name='output.zip', as_attachment=True)

@app.route('/', methods=['GET'])
def home():
    return form_html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
