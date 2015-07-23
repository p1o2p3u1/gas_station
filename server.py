from flask import Flask, jsonify, request, current_app
from functools import wraps
from file_handler import FileHandler

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
    return "hello world"

@app.route('/file/<filename>')
@jsonp
def get_source(filename):
    f = FileHandler()
    return jsonify(f.get_source(filename))

@app.route('/list')
@jsonp
def list_dir():
    f = FileHandler()
    return jsonify(f.list_all_files())

if __name__ == '__main__':
    app.run(debug=True)
