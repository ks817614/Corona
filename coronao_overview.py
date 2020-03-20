import requests
import json
import time
from datetime import date
from prettytable import PrettyTable
import matplotlib.pyplot as plt

URL = "https://coronavirus-tracker-api.herokuapp.com/all"

COUNTRY_DICT = {
    'DE': 'Deutschland',
    'IT': 'Italien',
    'BE': 'Belgien',
    'CH': 'Schweiz',
    'AT': 'Östereich',
    'NL': 'Niederlande'
}
COUNTRY_POPULATION = {
    'WW': 7763035303,
    'DE': 82790000,
    'IT': 60480000,
    'BE': 11400000,
    'CH': 8570000,
    'AT': 8882000,
    'NL': 171800000
}

def print_time(parsed):
    last_update = repr(parsed.get("confirmed").get("last_updated"))
    date = last_update[1:11]
    time = last_update[12:20]
    print('Letzte Update: ' + date + ' ' + time)

def get_country_data(id, parsed):
    country_data = []
    country_code = repr(parsed.get("confirmed").get("locations")[id].get("country_code"))[1:3]
    country = COUNTRY_DICT[country_code]
    confirmed_c = int(repr(parsed.get("confirmed").get("locations")[id].get("latest")))
    deaths_c = repr(parsed.get("deaths").get("locations")[id].get("latest"))
    recovered_c = repr(parsed.get("recovered").get("locations")[id].get("latest"))
    lethality_c = (float(deaths_c)/float(confirmed_c))*100
    confirmed_in_percent_c = (float(confirmed_c)/COUNTRY_POPULATION[country_code]) * 100
    recovered_percent_c = (float(recovered_c)/float(confirmed_c))*100
    ill_c = int(confirmed_c) - int(deaths_c) - int(recovered_c)

    country_data.append(country)
    country_data.append(confirmed_c)
    country_data.append(ill_c)
    country_data.append(deaths_c)
    country_data.append(recovered_c)
    country_data.append("{:10.2f}".format(lethality_c))
    country_data.append("{:10.4f}".format(confirmed_in_percent_c))
    country_data.append("{:10.2f}".format(recovered_percent_c))

    return country_data


def get_country_id(parsed):
    country_id_list = []
    for i, data in enumerate(parsed.get("confirmed").get("locations")):
        if data['country_code'] in COUNTRY_DICT.keys():
            country_id_list.append(i)

    return country_id_list


def create_table(parsed):
    country_data = []
    confirmed_w = repr(parsed.get("latest").get("confirmed"))
    deaths_w = repr(parsed.get("latest").get("deaths"))
    recovered_w = repr (parsed.get("latest").get("recovered"))
    lethality_w = (float(deaths_w)/float(confirmed_w))*100
    confirmed_in_percent_w = (float(confirmed_w)/COUNTRY_POPULATION['WW']) * 100
    recovered_percent_w = (float(recovered_w)/float(confirmed_w))*100
    ill_w = int(confirmed_w) - int(deaths_w) - int(recovered_w)

    t = PrettyTable(['Land', 'Infektionen', 'Krank', 'Tode', 'Geheilt',
                     'Letalität [%]', 'Infizierte Bevölkerung[%]', 'Geheilt [%]'])
    t.add_row(['Weltweit', confirmed_w, ill_w, deaths_w,
               recovered_w, "{:10.2f}".format(lethality_w),
               "{:10.4f}".format(confirmed_in_percent_w),
               "{:10.2f}".format(recovered_percent_w)])

    country_id_list = get_country_id(parsed)

    for id in country_id_list:
        country_data.append(get_country_data(id, parsed))

    # sort by confirmed infection
    country_data.sort(key=lambda x: x[1], reverse=True)

    for country in country_data:
        t.add_row(country)
    return t


def get_data():
    response = requests.get(URL)
    data = response.text
    parsed = json.loads(data)
    return parsed


if __name__ == "__main__":
    parsed_data = get_data()
    print_time(parsed_data)
    table = create_table(parsed_data)
    print(table)