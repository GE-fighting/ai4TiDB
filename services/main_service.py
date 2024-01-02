# services/main_service.py
from models.model import LWNNModel
import torch

class MainService:
    def make_prediction(self):
        # 在这里调用你的深度学习模型进行预测
        # 处理数据
        feature = [500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0, 500.0000000000685, 500.0, 500.0, 500.0, 500.0000000000685, 368925.4703928945, 577530.8030984252, 904089.9999999999]
        # 假设这里有一个名为model的深度学习模型
        mlp_model = LWNNModel(15, "128_64_32").to("cpu")
        # 加载保存的模型状态字典
        checkpoint_path = '/home/code/python_projects/ai4TiDB/models/mlp_model_epoch1000.pth'
        checkpoint = torch.load(checkpoint_path)
        mlp_model.load_state_dict(checkpoint)
        # 设置模型为评估模式
        mlp_model.eval()
        input_data = torch.tensor(feature, dtype=torch.float)
        prediction = mlp_model(input_data)
        result = prediction.tolist()[0]
        return result