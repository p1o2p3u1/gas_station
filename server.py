from flask import Flask, jsonify, request, current_app
from functools import wraps
from app.file_handler import FileHandler

app = Flask(__name__)

def jsonp(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs).data)
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

@app.route('/')
def hello():
    return "Hello World"

@app.route('/file')
@jsonp
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
def list_dir():
    f = FileHandler()
    return jsonify(f.list_all_files())

if __name__ == '__main__':
    app.run(debug=True)
