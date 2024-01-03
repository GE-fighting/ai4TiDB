from flask import Flask, request
from controllers.main_controller import MainController

app = Flask(__name__)

# 初始化控制器
main_controller = MainController()

# 设置路由
@app.route('/')
def index():
    # 调用控制器的方法处理请求
    return main_controller.index()


@app.route('/predict', methods=['POST'])
def predict():
    request_body_string = request.data.decode('utf-8')
    return main_controller.predict(request_body_string)

if __name__ == '__main__':
    app.run(debug=True)