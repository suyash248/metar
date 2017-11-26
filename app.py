from flask import Flask, request

# Registering Flask application.
app = Flask(__name__)
from settings import APP
from views.metar import metar

# Routes -> Views blueprints
app.register_blueprint (metar, url_prefix='/metar')

@app.route("/")
@app.route("/metar")
def main():
    print request.host, request.host_url
    return "Welcome to METAR"

if __name__ == "__main__":
    app.run (host=APP.get('HOST', '0.0.0.0'), port=APP.get('PORT', 8080))