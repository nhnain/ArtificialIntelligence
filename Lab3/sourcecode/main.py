rs = "[1.2, 3.5, 5.8]"
rs = rs[rs.find("[")+1:rs.rfind("]")].split(",")
rs = [float(item) for item in rs]
print(rs[0])