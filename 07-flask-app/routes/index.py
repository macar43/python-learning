from flask import render_template
from routes import index_bp

@index_bp.route('/')
def home():
    return render_template('index.html', title='Home')

@index_bp.route('/about')
def about():
    return render_template('about.html', title='About')

@index_bp.route('/api/hello')
def api_hello():
    return {'message': 'Hello from Flask API!'}
