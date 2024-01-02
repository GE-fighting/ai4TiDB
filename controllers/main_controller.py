# controllers/main_controller.py

from flask import jsonify, request
from services.main_service import MainService


main_service = MainService()

class MainController:
    def index(self):
        data = {
            'name': 'jfpoei9',
        }
        return jsonify(data)

    def predict(self):
        # input_data = request.json
        prediction = main_service.make_prediction()
        print(prediction)
        return jsonify({'prediction': prediction})