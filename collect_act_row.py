import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="4000",
    passwd=""
)
cursor = db.cursor()

query_file = 'collected_query.json'
with open(query_file, 'r') as f:
    qs = json.load(f)

results = []
print(f'总长度是{len(qs)}')
i = 1
cursor.execute("set @@tidb_external_cardinality_estimator_address=''")
for q in qs:
    cursor.execute(q)
    act_num = cursor.fetchall()
    result = act_num[0][0]
    print(f'第{i}个语句')
    i = i + 1
    results.append(result)

cursor.close()

with open('collected_act_row.json', 'w') as outfile:
    json.dump(results, outfile)