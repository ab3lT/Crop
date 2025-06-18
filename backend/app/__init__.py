from flask import Flask
from .db import db
from .routes import routes

def create_app():
    app = Flask(__name__)

    # MySQL config (edit as needed)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@localhost:3306/crop'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u9qsf60cd9fnj6:p171f9844b77f6d8b58701c2ff575218d23a549ad19475a8a1296e872d8a545a6@c5cnr847jq0fj3.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2338e3bvk9s8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'AAiT CropYieldPrediction Project'

    db.init_app(app)
    app.register_blueprint(routes)

    return app
