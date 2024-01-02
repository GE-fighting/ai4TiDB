from flask import Flask, request, jsonify

app = Flask(__name__)

# 假设你已经有了一个模型状态字典，比如model_state
model_state = {
    'foo': 'bar',
    'baz': 'qux'
}

# 创建一个接收GET请求的端点
@app.route('/get_model_state', methods=['GET'])
def get_model_state():
    return jsonify(model_state)

# 创建一个接收POST请求的端点
@app.route('/update_model_state', methods=['POST'])
def update_model_state():
    data = request.get_json()
    # 假设请求的JSON数据格式为 {'key': 'new_value'}
    key = data.get('key')
    if key in model_state:
        model_state[key] = data['value']
        return 'Model state updated successfully'
    else:
        return 'Key not found in model state', 404

if __name__ == '__main__':
    app.run()