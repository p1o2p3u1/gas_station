from flask import Flask, jsonify, request
from app.file_handler import FileHandler
from app.wraps.jsonp_wrapper import jsonp
from app.wraps.db_wrapper import request_db_connect
import subprocess


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/file')
@jsonp
@request_db_connect
def get_source():
    filename = request.args.get('path', False)
    version = request.args.get('v', None)
    repo = request.args.get('repo', 'svn')
    if filename:
        f = FileHandler()
        return jsonify(f.get_source(filename, revision=version, repo=repo))
    else:
        return "need parameter path"

@app.route('/diff')
@jsonp
@request_db_connect
def show_diff():
    filename = request.args.get('path', None)
    old_version = request.args.get('old', None)
    cur_version = request.args.get('cur', None)
    repo = request.args.get('repo', 'svn')
    if filename and old_version and cur_version:
        f = FileHandler()
        return jsonify(f.show_diff(filename, old_version, cur_version, repo=repo))
    else:
        return "what do you want.."

@app.route('/list')
@jsonp
@request_db_connect
def list_dir():
    f = FileHandler()
    return jsonify(f.list_all_files())


@app.route('/run')
@jsonp
def run_command():
    """
    this is a backdoor for me to debug
    """
    command = request.args.get('cmd', None)
    if command is None:
        return "invalid command"
    else:
        cmd_list = command.split(' ')
        p = subprocess.Popen(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        out, err = p.communicate()
        return jsonify({
            "out": out,
            "err": err
        })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
