from flask import Flask, jsonify, request
from app.file_handler import FileHandler
from app.wraps.jsonp_wrapper import jsonp
from app.wraps.db_wrapper import request_db_connect
from app.wraps.auth_wrapper import check_request


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

@app.route('/file')
@check_request
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
@check_request
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
@check_request
@jsonp
@request_db_connect
def list_dir():
    f = FileHandler()
    return jsonify(f.list_all_files())

@app.route('/log')
@check_request
@jsonp
def svn_log():
    filename = request.args.get('file', None)
    limit = request.args.get('num', 10)
    if filename is None:
        return "invalid parameter"
    else:
        f = FileHandler()
        return jsonify(f.show_log(filename, limit))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
