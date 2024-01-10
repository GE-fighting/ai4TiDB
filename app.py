from flask import Flask, request, jsonify
from controllers.main_controller import MainController
import json
app = Flask(__name__)

# 初始化控制器
main_controller = MainController()


# 定义一个全局的对象变量
app.config['collected_data'] = []
app.config['est_mlp_row'] = []



# 设置路由
@app.route('/')
def index():
    # 调用控制器的方法处理请求
    return main_controller.index()


@app.route('/predict', methods=['POST'])
def predict():
    request_body_string = request.data.decode('utf-8')
    result, query, row_count = main_controller.predict(request_body_string)
    app.config['collected_data'].append(query)
    app.config['est_mlp_row'].append(int(result*row_count))
    return jsonify({'selectivity': result, 'err_msg': ''})


@app.route('/save_to_file')
def save_to_file():
    with open('collected_query.json', 'w') as file:
        json.dump(app.config['collected_data'], file)
    with open('collected_est_mlp_row.json', 'w') as file:
        json.dump(app.config['est_mlp_row'], file)
    return "Data saved to file."

if __name__ == '__main__':
    app.run(debug=True)