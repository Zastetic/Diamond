from flask import Flask
from routes import bp
from datetime import timedelta

app = Flask(__name__)
app.register_blueprint(bp)

app.secret_key = 'segredo_super_secreto'

if __name__ == "__main__":
    app.run(debug=True)