# import csv
# from pprint import pprint

# f = open('Data/portfolio.csv')
# f_csv = csv.reader(f)
# headers = next(f_csv)
# print(headers)
# rows = list(f_csv)
# pprint(rows)


import csv
import tracemalloc


tracemalloc.start()
f = open('Data/ctabus.csv')
f_csv = csv.reader(f)
headers = next(f_csv)
rows = (dict(zip(headers,row)) for row in f_csv)
rt22 = (row for row in rows if row['route'] == '22')
max(rt22, key=lambda row: int(row['rides']))
print("used memory:\n- current: {}b\n- peak: {}b".format(*tracemalloc.get_traced_memory()))