from flask import Flask
from flask_restful import Api
import simplejson

from resources import HolidayOffers


class HolidayOffersAppConfig:
    RESTFUL_JSON = {'cls': simplejson.JSONEncoder}


def create_app():
    app = Flask(__name__)
    app.config.from_object(HolidayOffersAppConfig)

    api = Api(app)

    api.add_resource(
        HolidayOffers, '/holiday_offers', endpoint='holiday-offers'
    )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
