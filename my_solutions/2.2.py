import csv
import tracemalloc
from collections import Counter, defaultdict

class Row:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

def read_rides_as_tuples(filename):
    '''
    Read the bus ride data as a list of tuples
    '''
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _ = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = Row(route, date, daytype, rides)
            records.append(record)
    return records

if __name__ == '__main__':
    tracemalloc.start()
    rows = read_rides_as_tuples('Data/ctabus.csv')
    current, peak = tracemalloc.get_traced_memory()
    print(f'Memory Use: Current {current/1e6:.3f}MB, Peak {peak/1e6:.3f}MB')

    routes = {row.route for row in rows}

    print("How many bus routes exist in Chicago? -> {}".format(len(routes)))

    feb_2_2011 = [row.rides for row in rows if row.date == "02/02/2011" and row.route == "22"]

    print("How many people rode the number 22 bus on February 2, 2011? What about any route on any date of your choosing? -> {}".format(sum(feb_2_2011)))

    couted_per_bus_route = Counter()
    for row in rows:
        couted_per_bus_route[row.route] += row.rides

    print("What is the total number of rides taken on each bus route? (top 3) -> {}".format(couted_per_bus_route.most_common(3)))

    couted_per_bus_route_2001 = Counter()
    couted_per_bus_route_2011 = Counter()
    print(rows[1].date[-4:])
    for row in rows:
        if (row.date[-4:] == "2001"):
            couted_per_bus_route_2001[row.route] += row.rides
        elif (row.date[-4:] == "2011"):
            couted_per_bus_route_2011[row.route] += row.rides

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