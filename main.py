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
    aqi = response_json['data']['aqi']
    level = 0
    if 0 <= aqi <= 50:
        level = "good"
    elif 51 <= aqi <= 100:
        level = "moderate"
    elif 101 <= aqi <= 150:
        level = "unhealthy for sensitive groups"
    elif 151 <= aqi <= 200:
        level = "unhealty"
    elif 201 < aqi <= 300:
        level = "very unhealthy"
    else:
        level = "hazardous"

    info = {
        "city": city,
        "aqi": response_json['data']['aqi'],
        "time": response_json['data']['time']['s'],
        "temperature": response_json['data']['iaqi']['t']['v'],
        "pressure": response_json['data']['iaqi']['p']['v'],
        "humidity": response_json['data']['iaqi']['h']['v'],
        "wind": response_json['data']['iaqi']['w']['v'],
        "masini": nr_cars,
        "level": level
    }
    return info


def write(data):
    with open("BD\\bd.json", "w") as fd:
        json.dump(data, fd, indent=4)
    with open("BD\\bd.json") as fd:
        info = json.load(fd)
        bd_csv = open('BD\\bd.csv', 'w')
        csv_writer = csv.writer(bd_csv)
        for index, item in enumerate(info):
            if index == 0:
                header = item.keys()
                csv_writer.writerow(header)
            csv_writer.writerow(item.values())
        bd_csv.close()


def get_coord(city):
    link = 'https://api.opencagedata.com/geocode/v1/json?key=4bda95c130604a9685ab01473f82b3d9&q='
    response = requests.get(
        f"https://api.opencagedata.com/geocode/v1/json?key=4bda95c130604a9685ab01473f82b3d9&q={city} Romania")
    response_json = response.json()
    return response_json['results'][0]['geometry']['lat'], response_json['results'][0]['geometry']['lng']


def add_coord(csv_file):
    with open(csv_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        content = []
        for row in csv_reader:
            if line_count == 0:
                row.append("lat")
                row.append("lng")
                content.append(", ".join(row))
                line_count += 1
            else:
                lat, lng = get_coord(row[2])
                row.append(str(lat))
                row.append(str(lng))
                content.append(", ".join(row))
                line_count += 1
        print(f'Processed {line_count} lines.')
    with open('BD\\riof.csv', 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, delimiter="\n")
        wr.writerow(content)


def get_number_of_cars(path):
    judete = {}
    with open(path, "r") as fd:
        csv_reader = csv.DictReader(fd)
        for row in csv_reader:
            judete[row["Judet"].strip().upper()] = judete.get(row["Judet"], 0) + int(row['Valoare'])
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
    # add_coord("BD\\romanian_institution_of_statistics.csv")
