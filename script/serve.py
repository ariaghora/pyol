import os
import json
import subprocess

from flask import Flask, request

app = Flask(__name__)

script_path = os.path.abspath(__file__)
config = os.path.join(os.path.dirname(script_path), 'server.json')

def get_upload_folder():
    return json.loads(open(config,'r').read())['upload_folder']

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        ''' base folder in which the files are stored in the
            server side '''
        project_name = request.form.get('project_name')
        file = request.files['file']
        filename = file.filename
        path = request.form.get('path').replace('./', '')
        savedir = get_upload_folder()+'/'+project_name + \
                '/'+ os.path.dirname(path)

        ''' Create directory structure '''
        os.makedirs(savedir, exist_ok=True)

        ''' Actually save the file '''
        file.save(savedir+'/'+filename)
    return 'Not allowed operation'

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        path = request.form.get('path').replace('./', '')
        project_name = request.form.get('project_name')
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        deldir = get_upload_folder()+'/'+project_name+'/'+dirname
        os.remove(deldir+filename)

    return 'Not allowed operation'

@app.route('/execute', methods=['GET', 'POST'])
def execute():
    if request.method == 'POST':
        path = request.form.get('path').replace('./', '')
        project_name = request.form.get('project_name')
        dirname = os.path.dirname(path)
        filename = os.path.basename(path)
        execdir = get_upload_folder()+'/'+project_name+'/'+dirname
        execpath = execdir+filename
        lcmd = 'python %s'%execpath
        return subprocess.check_output(lcmd, stderr=subprocess.STDOUT)
    return 'Not allowed operation'

app.run(debug=1)
