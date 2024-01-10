import json

import evaluation_utils as eval_utils

model = 'mlp'

act_row, tidb_est_row, mlp_est_row = [], [], []
with open('../collected_act_row.json') as f:
    act_row = json.load(f)

with open('../collected_est_mlp_row.json') as f:
    mlp_est_row = json.load(f)


with open('../output.log', 'r') as file:
    # 读取日志文件中的所有行
    tidb_est_row_str = file.readlines()
for str in tidb_est_row_str:
    tidb_est_row.append(int(str))


name = 'tidb_est'
eval_utils.draw_act_est_figure(name, act_row, tidb_est_row)
p50, p80, p90, p95, p99 = eval_utils.cal_p_error_distribution(act_row, tidb_est_row)
print(f'{name}, p50:{p50}, p80:{p80}, p90:{p90}, p95:{p95}, max:{p99}')

name = 'mlp_est'
eval_utils.draw_act_est_figure(name, act_row, mlp_est_row)
p50, p80, p90, p95, p99 = eval_utils.cal_p_error_distribution(act_row, mlp_est_row)
print(f'{name}, p50:{p50}, p80:{p80}, p90:{p90}, p95:{p95}, max:{p99}')