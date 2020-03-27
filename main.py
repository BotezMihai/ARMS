import requests
import json
import csv

counties = [
    "ALBA", "ARAD", "ARGES", "BACAU", "BIHOR", "BISTRITA - NASAUD", "BOTOSANI", "BRASOV", "BRAILA", "BUZAU",
    "CARAS-SEVERIN", "CALARASI", "CLUJ", "CONSTANTA", "COVASNA", "DAMBOVITA", "DOLJ", "GALATI", "GIURGIU", "GORJ",
    "HARGHITA", "HUNEDOARA", "IALOMITA", "IASI", "ILFOV", "MARAMURES", "MEHEDINTI", "MURES", "NEAMT", "OLT", "PRAHOVA",
    "SATU MARE", "SALAJ", "SIBIU", "SUCEAVA", "TELEORMAN", "TIMIS", "TULCEA", " VASLUI", "VALCEA", "VRANCEA",
    "BUCURESTI"]


def get_response(city):
    response = requests.get(f"https://api.waqi.info/feed/{city}/?token=15fa9a97cfe55a721c7c22f24394ae4a68a879be")
    response_json = response.json()
    if response_json['status'] != 'ok':
        return "City not found"
    info = {"aqi": response_json['data']['aqi'], "time": response_json['data']['time']['s'], "city": city}
    return info


def write(data):
    with open("BD\\bd.json", "w") as fd:
        json.dump(data, fd)


if __name__ == '__main__':
    info = get_response("Iasi")
    with open("BD\\bd.json") as fd:
        data = json.load(fd)
        for i in counties:
            info = get_response(i)
            data.append(info)
        with open('BD\\bd.csv', 'w') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(data)
        write(data)
