import json
from math import sqrt
import sys


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_with_json:
        return json.load(file_with_json)


def take_seat_count_bar(data_bar):
    return data_bar['properties']['Attributes']['SeatsCount']


def get_smallest_bar(data_from_file):
    return min(data_from_file, key=lambda x: take_seat_count_bar(x))


def get_biggest_bar(data_from_file):
    return max(data_from_file, key=lambda x: take_seat_count_bar(x))


def get_closest_bar(data_from_file, longitude, latitude):
    return min(data_from_file,
               key=lambda x: (calculate_distance(longitude,
                                                 latitude,
                                                 *x['geometry']['coordinates'])))


def calculate_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    return sqrt((x_coord_1-x_coord_2)**2 + (y_coord_1-y_coord_2)**2)


def get_user_coordinate():
    print('Введите ваши координаты x,y= ')
    try:
        x, y = input().split(',')
        coordinate_x, coordinate_y = float(x), float(y)
        return coordinate_x, coordinate_y
    except ValueError:
        raise ValueError


def print_bar_name(bar_discript, bar):
    print('{} {}'.format(bar_discript, bar['properties']['Attributes']['Name']))


if __name__ == '__main__':
    try:
        data_from_json_file = load_data(sys.argv[1])['features']
        user_coordinate = get_user_coordinate()
        biggest_bar = get_biggest_bar(data_from_json_file)
        smallest_bar = get_smallest_bar(data_from_json_file)
        closest_bar = get_closest_bar(data_from_json_file, *user_coordinate)
        print_bar_name('Большой бар: ', biggest_bar)
        print_bar_name('Маленький бар: ', smallest_bar)
        print_bar_name('Ближайщий бар: ', closest_bar)
    except (FileNotFoundError, IndexError):
        print('Ошибка: Вы не добавили файл!')
    except json.decoder.JSONDecodeError:
        print('Ошибка: Расширение файла не JSON!')
    except ValueError:
        print('Ошибка ввода координат')

