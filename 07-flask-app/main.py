from flask import Flask, render_template
from config import Config
from routes import index_bp

app = Flask(__name__)
app.config.from_object(Config)

# Blueprint registrieren
app.register_blueprint(index_bp)

if __name__ == '__main__':
    app.run(debug=True)
