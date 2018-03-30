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
               key=lambda x: (calculate_distance(
                   longitude,
                   latitude,
                   *x['geometry']['coordinates']))
               )


def calculate_distance(x_coord_1, y_coord_1, x_coord_2, y_coord_2):
    return sqrt((x_coord_1-x_coord_2)**2 + (y_coord_1-y_coord_2)**2)


def get_user_coordinate():
    print('Введите ваши координаты x,y= ')
    try:
        x, y = input().split(',')
        coordinate_x, coordinate_y = float(x), float(y)
        return coordinate_x, coordinate_y
    except ValueError:
        return None


def print_bar_name(bar_discript, bar):
    print('{} {}'.format(bar_discript, bar['properties']['Attributes']['Name']))


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
        user_coordinate = get_user_coordinate()
        print_bar_name('Самый большой бар:',
                       get_biggest_bar(info_bars))
        print_bar_name('Самый маленький бар:',
                       get_smallest_bar(info_bars))
        if user_coordinate:
            print_bar_name('Самый близкий бар:',
                           get_closest_bar(info_bars, *user_coordinate))
        else:
            print('Самый близкий бар не был найден из-за'
                  'ошибки ввода координат')
