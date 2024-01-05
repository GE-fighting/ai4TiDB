# controllers/main_controller.py

from flask import jsonify
from services.main_service import MainService


main_service = MainService()

class MainController:
    def index(self):
        data = {
            'name': 'jfpoei9',
        }
        return jsonify(data)

    def predict(self, conds):
        # input_data = request.json
        prediction, query = main_service.make_prediction(conds)
        return prediction, query
