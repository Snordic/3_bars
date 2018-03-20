import json
from math import sqrt
import sys


def input_user_coordinate():
    print('Введите ваши координаты x,y= ')
    coordinate_x, coordinate_y = input().split(',')
    return float(coordinate_x), float(coordinate_y)


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file_with_json:
            data_from_file = json.load(file_with_json)
    except TypeError:
        print('Ошибка: Вы не добавили файл!')
    except json.decoder.JSONDecodeError:
        print('Ошибка: Расширение файла не JSON!')
    else:
        return data_from_file['features']


def get_biggest_bar(data_from_json_file):
    biggest_bar = max(data_from_json_file,
                      key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(data_from_json_file):
    smallest_bar = min(data_from_json_file,
                       key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar(data_from_json_file):
    try:
        longitude, latitude = input_user_coordinate()
    except ValueError:
        print('Ошибка: Координаты должны быть числами и вводится через запятую!')
        return 'Не подсчитан из-за ошибки'
    else:
        closest_bar = min(data_from_json_file,
                          key=lambda x: (calculate_distance(longitude,
                                                            latitude,
                                                            *x['geometry']['coordinates']
                                                            )))
        return closest_bar['properties']['Attributes']['Name']


def calculate_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    distance_bar = sqrt(
        (x_coord_1-x_coord_2)**2 + (y_coord_1-y_coord_2)**2)
    return distance_bar


def print_search_bar(data_from_json_file):
    try:
        print(' Самый большой бар: ' + get_biggest_bar(data_from_json_file) +
              ';\n Самый маленький бар: ' + get_smallest_bar(data_from_json_file) +
              ';\n Самый близкий бар: ' + get_closest_bar(data_from_json_file)
              )
    except TypeError:
        print('Ошибка: Не добавлен файл bars.json')



if __name__ == '__main__':
    try:
        #filename = 'bars.json'
        filename = sys.argv[1]
    except IndexError:
        print('Ошибка: Не добавлен JSON файл с данными!')
    else:
        print_search_bar(load_data(filename))
