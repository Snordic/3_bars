import json
from math import sqrt
import sys


def input_user_coordinate():
    print('Введите ваши координаты x,y= ')
    try:
        x, y = input().split(',')
        coordinate_x, coordinate_y = float(x), float(y)
    except ValueError:
        print('Ошибка: Координаты должны быть числами и вводится через запятую!')
        return None, None
    else:
        return coordinate_x, coordinate_y


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file_with_json:
            data_from_file = json.load(file_with_json)
    except FileNotFoundError:
        print('Ошибка: Данный файл не существует!')
        return None
    except json.decoder.JSONDecodeError:
        print('Ошибка: Расширение файла не JSON!')
        return None
    else:
        return data_from_file['features']


def get_biggest_bar(data_from_file):
    biggest_bar = max(data_from_file,
                      key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar


def get_smallest_bar(data_from_file):
    smallest_bar = min(data_from_file,
                       key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return smallest_bar


def get_closest_bar(data_from_file):
    longitude, latitude = input_user_coordinate()
    if longitude and latitude:
        closest_bar = min(data_from_file,
                          key=lambda x: (calculate_distance(
                              longitude,
                              latitude,
                              *x['geometry']['coordinates']))
                          )
        return closest_bar
    else:
        return None


def calculate_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    distance_bar = sqrt(
        (x_coord_1-x_coord_2)**2 + (y_coord_1-y_coord_2)**2
    )
    return distance_bar


def search_name_bar(filename):
    data_from_json_file = load_data(filename)
    if data_from_json_file:
        biggest_bar = get_biggest_bar(data_from_json_file)
        smallest_bar = get_smallest_bar(data_from_json_file)
        closest_bar = get_closest_bar(data_from_json_file)
        name_biggest_bar = biggest_bar['properties']['Attributes']['Name']
        name_smallest_bar = smallest_bar['properties']['Attributes']['Name']
        if closest_bar:
            name_closest_bar = closest_bar['properties']['Attributes']['Name']
        else:
            name_closest_bar = 'Бар не найден из-за ошибки ввода координат!'
        return name_biggest_bar, name_smallest_bar, name_closest_bar
    else:
        return None, None, None


def print_search_bar(biggest_bar, smallest_bar, closest_bar):
    print('{} {}'.format('Самый большой бар:', biggest_bar))
    print('{} {}'.format('Самый маленький бар:', smallest_bar))
    print('{} {}'.format('Самый близкий к вам бар:', closest_bar))


def main(filename):
    big_bar, small_bar, closest_bar = search_name_bar(filename)
    if big_bar and small_bar and closest_bar:
        print_search_bar(big_bar, small_bar, closest_bar)


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Ошибка: Вы не добавили файл JSON!')
    else:
        main(filename)
