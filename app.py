from flask import Flask, render_template, request, send_from_directory
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

app = Flask(__name__)

# ======================
# ROUTE XML FILE
# ======================
@app.route('/transport.xml')
def transport_xml():
    return send_from_directory(
        os.path.dirname(os.path.abspath(__file__)),
        'transport.xml'
    )

XML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transport.xml')

# ======================
# LOAD XML
# ======================
def load_tree():
    return ET.parse(XML_FILE)

# ======================
# GET STATION NAME
# ======================
def get_station_name(root, station_id):
    for s in root.find('stations'):
        if s.get('id') == station_id:
            return s.get('name')
    return station_id

# ======================
# GET TRIP BY CODE
# ======================
def get_trip_by_code(code):
    dom = minidom.parse(XML_FILE)
    trips = dom.getElementsByTagName('trip')

    for trip in trips:
        if trip.getAttribute('code') == code:
            schedule = trip.getElementsByTagName('schedule')[0]

            return {
                'code': code,
                'type': trip.getAttribute('type'),
                'departure': schedule.getAttribute('departure'),
                'arrival': schedule.getAttribute('arrival')
            }
    return None

# ======================
# FILTER TRIPS
# ======================
def filter_trips(departure=None, arrival=None, train_type=None, max_price=None):
    tree = load_tree()
    root = tree.getroot()

    results = []

    for line in root.find('lines'):
        dep_id = line.get('departure')
        arr_id = line.get('arrival')

        dep_name = get_station_name(root, dep_id)
        arr_name = get_station_name(root, arr_id)

        if departure and departure.lower() != dep_name.lower():
            continue
        if arrival and arrival.lower() != arr_name.lower():
            continue

        for trip in line.find('trips'):

            if train_type and train_type.lower() != trip.get('type').lower():
                continue

            # ✅ FIX PRICE PARSING (IMPORTANT)
            prices = []
            for c in trip.findall('class'):
                raw_price = c.get('price')
                clean_price = raw_price.replace('DA', '').strip()
                prices.append(int(clean_price))

            min_price = min(prices) if prices else 0

            if max_price and min_price > int(max_price):
                continue

            results.append({
                'code': trip.get('code'),
                'type': trip.get('type'),
                'departure': dep_name,
                'arrival': arr_name,
                'time_dep': trip.find('schedule').get('departure'),
                'time_arr': trip.find('schedule').get('arrival'),
                'price': min_price
            })

    return results

# ======================
# STATISTICS
# ======================
def get_stats():
    tree = load_tree()
    root = tree.getroot()

    stats = {}
    types_count = {}

    for line in root.find('lines'):
        line_code = line.get('code')
        prices = []

        for trip in line.find('trips'):
            t_type = trip.get('type')
            types_count[t_type] = types_count.get(t_type, 0) + 1

            for c in trip.findall('class'):
                raw_price = c.get('price')
                clean_price = raw_price.replace('DA', '').strip()
                prices.append(int(clean_price))

        if prices:
            stats[line_code] = {
                'min': min(prices),
                'max': max(prices)
            }

    return stats, types_count

# ======================
# MAIN ROUTE
# ======================
@app.route('/', methods=['GET', 'POST'])
def index():
    trips = []
    trip = None
    stats, types = get_stats()

    if request.method == 'POST':
        code = request.form.get('code')
        departure = request.form.get('departure')
        arrival = request.form.get('arrival')
        train_type = request.form.get('type')
        max_price = request.form.get('price')

        if code:
            trip = get_trip_by_code(code)
        else:
            trips = filter_trips(departure, arrival, train_type, max_price)

    return render_template(
        'index.html',
        trips=trips,
        trip=trip,
        stats=stats,
        types=types
    )

# ======================
# RUN APP
# ======================
if __name__ == '__main__':
    app.run(debug=True)