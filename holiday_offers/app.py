from flask import Flask
from flask_restful import Api

from resources import HolidayOffers


def create_app():
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(
        HolidayOffers, '/holiday_offers', endpoint='holiday-offers'
    )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
