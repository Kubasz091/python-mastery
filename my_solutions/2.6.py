from reader import read_csv_as_dicts
import csv
import tracemalloc
from collections import Counter, defaultdict
from sys import intern

# portfolio = read_csv_as_dicts('Data/portfolio.csv', [str,int,float])

# for s in portfolio:
#     print(s)

# rows = read_csv_as_dicts('Data/ctabus.csv', [str,str,str,int])

# print(len(rows))
# print(rows[0])

if __name__ == '__main__':
    tracemalloc.start()
    rows = read_csv_as_dicts('Data/ctabus.csv', [intern,intern,intern,int])
    current, peak = tracemalloc.get_traced_memory()
    print(f'Memory Use: Current {current/1e6:.3f}MB, Peak {peak/1e6:.3f}MB')

    routes = {row["route"] for row in rows}

    print("How many bus routes exist in Chicago? -> {}".format(len(routes)))

    feb_2_2011 = [row["rides"] for row in rows if row["date"] == "02/02/2011" and row["route"] == "22"]

    print("How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing? -> {}".format(sum(feb_2_2011)))

    couted_per_bus_route = Counter()
    for row in rows:
        couted_per_bus_route[row["route"]] += row["rides"]

    print("What is the total number of rides taken on each bus route? (top 3) -> {}".format(couted_per_bus_route.most_common(3)))

    couted_per_bus_route_2001 = Counter()
    couted_per_bus_route_2011 = Counter()
    print(rows[1]["date"][-4:])
    for row in rows:
        if (row['date'][-4:] == "2001"):
            couted_per_bus_route_2001[row["route"]] += row["rides"]
        elif (row["date"][-4:] == "2011"):
            couted_per_bus_route_2011[row["route"]] += row["rides"]

    all_keys = {key for key in couted_per_bus_route_2001.keys()}
    for key in couted_per_bus_route_2011.keys():
        all_keys.add(key)
    print(all_keys)
    common_keys = {key for key in all_keys if key in couted_per_bus_route_2001.keys() and key in couted_per_bus_route_2011.keys()}

    print("15" in common_keys)
    print("15" in all_keys)
    print("15" in couted_per_bus_route_2001)
    print("15" in couted_per_bus_route_2011)
    # common_keys.add("15")

    print(couted_per_bus_route_2011['15'], "   ooooooooooo")

    diffs = Counter()
    for key in common_keys:
        diffs[key] = couted_per_bus_route_2011[key] - couted_per_bus_route_2001[key]


    print("What five bus routes had the greatest ten-year increase in ridership from 2001 to 2011? -> {}".format(diffs.most_common(5)))

    print(*(f"route: {row["route"]}, date: {row["date"]}" for row in rows[0:10]), sep="\n")