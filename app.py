import os
import logging
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

logs_folder = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

log_file = os.path.join(logs_folder, 'app.log')
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    query = request.form["q"]

    logging.info(f'Search query: {query}')

    location = requests.get(
        "https://nominatim.openstreetmap.org/search",
        {"q": query, "format": "json", "limit": "1"},
    ).json()

    if location:
        coordinate = [location[0]["lat"], location[0]["lon"]]

        time = requests.get(
            "https://timeapi.io/api/Time/current/coordinate",
            {"latitude": coordinate[0], "longitude": coordinate[1]},
        )

        logging.info(f'Successful search for location: {location[0]["display_name"]}')

        return render_template("success.html", location=location[0], time=time.json())

    else:
        logging.warning(f'No location found for query: {query}')
        return render_template("fail.html")

if __name__ == "__main__":
    app.run(debug=True)
