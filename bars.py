import json
from math import sqrt
import sys
import operator


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
    with open(filepath, 'r', encoding='utf-8') as file_with_json:
        return json.load(file_with_json)


def take_seat_count_bar(data_bar):
    return data_bar['properties']['Attributes']['SeatsCount']


def get_biggest_bar(information_bar):
    return max(information_bar,key=lambda x: (take_seat_count_bar(x)))


def get_smallest_bar(information_bar):
    return min(information_bar, key=lambda x: (take_seat_count_bar(x)))


def get_closest_bar(information_bar):
    longitude, latitude = input_user_coordinate()
    if longitude and latitude:
        return min(information_bar, key=lambda x: (calculate_distance(
            longitude,
            latitude,
            *x['geometry']['coordinates']))
                   )
    else:
        return None


def calculate_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    return sqrt((x_coord_1-x_coord_2)**2 + (y_coord_1-y_coord_2)**2)


def bar_name(data_bar):
    if data_bar:
        return data_bar['properties']['Attributes']['Name']
    else:
        return None


def get_names_bars(info_bars):
    name_biggest_bar = bar_name(get_biggest_bar(info_bars))
    name_smallest_bar = bar_name(get_smallest_bar(info_bars))
    name_closest_bar = bar_name(get_closest_bar(info_bars))
    if not name_closest_bar:
        name_closest_bar = 'Бар не найден из-за ошибки ввода координат!'
    return name_biggest_bar, name_smallest_bar, name_closest_bar


def print_search_bar(biggest_bar, smallest_bar, closest_bar):
    print('{} {}'.format('Самый большой бар:', biggest_bar))
    print('{} {}'.format('Самый маленький бар:', smallest_bar))
    print('{} {}'.format('Самый близкий к вам бар:', closest_bar))


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        data_from_json_file = load_data(filename)
        info_bars = data_from_json_file['features']
    except IndexError:
        print('Ошибка: Вы не добавили файл JSON!')
    except FileNotFoundError:
        print('Ошибка: Данный файл не существует!')
    except json.decoder.JSONDecodeError:
        print('Ошибка: Расширение файла не JSON!')
    else:
        print_search_bar(*get_names_bars(info_bars))
