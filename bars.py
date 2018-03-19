import json
from math import sqrt
import sys


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_with_json:
        data_from_file = json.load(file_with_json)
    return data_from_file['features']


def get_biggest_bar(data_json):
    biggest_bar = max(data_json,
                      key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(data_json):
    smallest_bar = min(data_json,
                       key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar(data_json, longitude, latitude):
    closest_bar = min(data_json,
                      key=lambda x: sqrt(
                          (longitude-x['geometry']['coordinates'][0])**2 +
                          (latitude-x['geometry']['coordinates'][1])**2)
                      )
    return closest_bar['properties']['Attributes']['Name']


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        data_json = load_data(filename)
    except IndexError: print('Ошибка: Вы не добавили файл!')
    except TypeError: print('Ошибка: Вы не добавили файл!')
    except json.decoder.JSONDecodeError: print('Ошибка: Расширение файла не JSON!')
    else:
        print('Введите ваши координаты x,y= ')
        coordinate_x, coordinate_y = input().split(',')
        data_json = load_data(filename)
        print(' Самый большой бар: ' + get_biggest_bar(data_json) +
              ';\n Самый маленький бар: ' + get_smallest_bar(data_json) +
              ';\n Самый близкий бар: ' +
              get_closest_bar(data_json, float(coordinate_x), float(coordinate_y)))