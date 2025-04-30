# app/main.py
from flask import Flask
from .routes import routes   # ← importación relativa

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
