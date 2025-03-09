import os
import pandas as pd
cur_path = os.getcwd()
result_path = os.path.join(cur_path, "result")

def parse_result_file(filename):
    try:
        file1 = open(filename, 'r') 
        lines = file1.readlines()
        file1.close()
        while True:
            rs = lines[-1].strip()
            if len(rs) != 0:
                break
        rs = rs[rs.find("[") + 1:rs.rfind("]")].split(",")
        rs = [float(item) for item in rs]
        return rs
    except:
        return -1

rows = []
for sidx in os.listdir(result_path):
    if sidx.startswith("."):
        continue
    rs_file = os.path.join(result_path, sidx, "result.txt")
    result = parse_result_file(rs_file)
    print(sidx, result)
    arow = {"ID": sidx}
    if result != -1: #has result
        total = 0
        for qidx, qscore in enumerate(result):
            col_name = "Q{:02d}".format(qidx + 1)
            arow[col_name] = qscore
            total += qscore
        arow["Total"] = total
    else:
        arow["Total"] = 0.0
    rows.append(arow)

table = pd.DataFrame(rows)
table.to_csv('report.csv')
