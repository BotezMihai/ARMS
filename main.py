import requests
import json
import csv

counties = [
    "ALBA", "ARAD", "ARGES", "BACAU", "BIHOR", "BISTRITA-NASAUD", "BOTOSANI", "BRASOV", "BRAILA", "BUZAU",
    "CARAS-SEVERIN", "CALARASI", "CLUJ", "CONSTANTA", "COVASNA", "DAMBOVITA", "DOLJ", "GALATI", "GIURGIU", "GORJ",
    "HARGHITA", "HUNEDOARA", "IALOMITA", "IASI", "ILFOV", "MARAMURES", "MEHEDINTI", "MURES", "NEAMT", "OLT", "PRAHOVA",
    "SATU MARE", "SALAJ", "SIBIU", "SUCEAVA", "TELEORMAN", "TIMIS", "TULCEA", "VASLUI", "VALCEA", "VRANCEA",
    "BUCURESTI", "DEVA"]


def get_response(city, nr_cars):
    response = requests.get(f"https://api.waqi.info/feed/{city}/?token=15fa9a97cfe55a721c7c22f24394ae4a68a879be")
    response_json = response.json()
    if response_json['status'] != 'ok':
        return None
    info = {
        "city": city,
        "aqi": response_json['data']['aqi'],
        "time": response_json['data']['time']['s'],
        "temperature": response_json['data']['iaqi']['t']['v'],
        "pressure": response_json['data']['iaqi']['p']['v'],
        "humidity": response_json['data']['iaqi']['h']['v'],
        "wind": response_json['data']['iaqi']['w']['v'],
        "masini": nr_cars
    }
    return info


def write(data):
    with open("BD\\bd.json", "w") as fd:
        json.dump(data, fd, indent=4)
    with open('BD\\bd.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)


def get_number_of_cars(path):
    judete = {}
    with open(path, "r") as fd:
        csv_reader = csv.DictReader(fd)
        for row in csv_reader:
            judete[row["Judet"].strip().upper()] = judete.get(row["Judet"], 0)+int(row['Valoare'])
    return judete


if __name__ == '__main__':
    nr_cars = get_number_of_cars('BD\\romanian_institution_of_statistics.csv')
    data = []
    for county in counties:
        county = county.strip().upper()

        if nr_cars.get(county):
            info = get_response(county, nr_cars[county])

            if info == None:
                print(f"The county {county} not found!")
                continue

            print(county)

            data.append(info)
        else:
            print(f"The county {county} not found!")

    write(data)
