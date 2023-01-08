import os
from flask import Flask
from datetime import timedelta
from routes import routes
from extensions import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(routes, url_prefix="/")
app.secret_key = os.environ["KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)

app.app_context().push()

db.init_app(app)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)