
from flask import Flask, render_template, request, send_from_directory
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

XML_FILE = os.path.join(os.path.dirname(__file__), 'transport.xml')

# ======================
# SERVE XML
# ======================
@app.route('/transport.xml')
def transport_xml():
    return send_from_directory(os.path.dirname(__file__), 'transport.xml')

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
# SEARCH BY CODE
# ======================
def get_trip_by_code(code):
    tree = load_tree()
    root = tree.getroot()

    for line in root.find('lines'):
        dep_id = line.get('departure')
        arr_id = line.get('arrival')

        dep_name = get_station_name(root, dep_id)
        arr_name = get_station_name(root, arr_id)

        for trip in line.find('trips'):
            if trip.get('code') == code:
                schedule = trip.find('schedule')

                return {
                    'code': code,
                    'type': trip.get('type'),
                    'departure': dep_name,
                    'arrival': arr_name,
                    'time_dep': schedule.get('departure'),
                    'time_arr': schedule.get('arrival')
                }
    return None

# ======================
# FILTER
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

            prices = []
            for c in trip.findall('class'):
                price = int(c.get('price').replace('DA', '').strip())
                prices.append(price)

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
# HOME + SEARCH
# ======================
@app.route('/', methods=['GET', 'POST'])
def index():
    trips = []
    trip = None

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

    return render_template('index.html', trips=trips, trip=trip)

# ======================
# RUN
# ======================
if __name__ == '__main__':
    app.run(debug=True)
