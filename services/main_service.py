# services/main_service.py
from models.model import LWNNModel
import torch
import services.statistics as stats
import services.range_query as rq


from flask import g
class MainService:
    def make_prediction(self, conds_str):
        # 处理conds:  “a > 1 and b < 9 and c >100 ....”
        query = 'select count(*) from imdb.title where ' + conds_str
        print(query)
        # record = {'sql': query}
        feature = []
        range_query = rq.ParsedRangeQuery.parse_range_query(query)
        col_left = range_query.col_left
        col_right = range_query.col_right
        considered_cols = ['kind_id', 'production_year', 'imdb_id', 'episode_of_id', 'season_nr', 'episode_nr']
        stats_json_file = './models/title_stats.json'
        table_stats = stats.TableStats.load_from_json_file(stats_json_file, considered_cols)
        for col in considered_cols:
            if col in col_left:
                feature.append(min_max_normalize(col_left[col], stats.MIN_VAL, stats.MAX_VAL) * 50)
            else:
                feature.append(
                    min_max_normalize(table_stats.columns[col].min_val(), stats.MIN_VAL, stats.MAX_VAL) * 50)
            if col in col_right:
                feature.append(min_max_normalize(col_right[col], stats.MIN_VAL, stats.MAX_VAL) * 50)
            else:
                feature.append(
                    min_max_normalize(table_stats.columns[col].max_val(), stats.MIN_VAL, stats.MAX_VAL) * 50)
        feature.append(stats.AVIEstimator.estimate(range_query, table_stats) * table_stats.row_count)
        feature.append(stats.ExpBackoffEstimator.estimate(range_query, table_stats) * table_stats.row_count)
        feature.append(stats.MinSelEstimator.estimate(range_query, table_stats) * table_stats.row_count)

        # 在这里调用你的深度学习模型进行预测
        # 假设这里有一个名为model的深度学习模型
        mlp_model = LWNNModel(15, "128_64_32").to("cpu")
        # 加载保存的模型状态字典
        checkpoint_path = '/home/code/python_projects/ai4TiDB/models/mlp_model_epoch500.pth'
        checkpoint = torch.load(checkpoint_path)
        mlp_model.load_state_dict(checkpoint)
        # 设置模型为评估模式
        mlp_model.eval()
        input_data = torch.tensor(feature, dtype=torch.float)
        prediction = mlp_model(input_data)
        result = prediction.tolist()[0]/table_stats.row_count
        return result, query, table_stats.row_count

def min_max_normalize(v, min_v, max_v):
     # The function may be useful when dealing with lower/upper bounds of columns.
     assert max_v > min_v
     return (v - min_v) / (max_v - min_v)
