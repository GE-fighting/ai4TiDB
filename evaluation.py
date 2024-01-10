import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="4000",
    passwd=""
)
cursor = db.cursor()

query_file = './models/workload.json'
with open(query_file, 'r') as f:
    qs = json.load(f)

cursor.execute("set @@tidb_external_cardinality_estimator_address='http://127.0.0.1:5000/predict'")
# cursor.execute("set @@tidb_external_cost_estimator_address='http://127.0.0.1:8888/cost'")

results = []
i = 1
for q in qs:
    cursor.execute("explain format='verbose' " + q)
    raw_plan = cursor.fetchall()
    print(f'第{i}个语句')
    i = i + 1
    # plan = []
    # for x in raw_plan:
    #     plan.append('\t'.join(x))
    # cursor.execute("show warnings")
    # warnings = cursor.fetchall()
    # ws = []
    # for w in warnings:
    #     ws.append('\t'.join([w[0], w[2]]))
    # result = {
    #     "query": q,
    #     "plan": plan,
    #     "warnings": ws
    # }
    # results.append(result)
    # print(result)

# with open('./eval/results.json', 'w') as outfile:
#     json.dump(results, outfile)
