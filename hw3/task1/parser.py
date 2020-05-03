import argparse
import os
import re
from prettytable import PrettyTable
from collections import Counter


class FileTypeException(Exception):
    pass


def log_check(_line, _regx):
    return _regx.match(_line)


def parse_line(_line):
    line_list = _line.replace('"', '').replace('[', '').replace(']', '').split(' ')[0:10]
    return [line_list[0], line_list[5], line_list[6], line_list[8], line_list[9]]


def process_file(filename):
    _log = []
    _methods = {}
    with open(filename) as file:
        if not log_check(file.readline(), regx):
            raise FileTypeException(f'{path} is not a nginx log')
        file.seek(0)
        for line in file.readlines():
            request = parse_line(line)
            if request[1] not in _methods.keys():
                _methods[request[1]] = 1
            else:
                _methods[request[1]] += 1
            _log.append(request)
    return _log, _methods


def count_overall(_log):
    tb = PrettyTable(['OVERALL REQUESTS COUNT'])
    tb.add_row([len(_log)])
    if args.output:
        with open(args.output, 'a') as file:
            file.write(str(tb))
    else:
        print(tb)


def count_by_type(_methods):
    tb = PrettyTable(['Method', 'Count'])
    tb.title = 'REQUESTS COUNT BY TYPE'
    for u, v in _methods.items():
        tb.add_row([u, v])
    if args.output:
        with open(args.output, 'a') as file:
            file.write(str(tb))
    else:
        print(tb)


def top10_by_size(_log):
    result_dict = dict(Counter([f'{i[2]} {i[3]} {i[4]}' for i in _log]))
    result_list = sorted([f'{v} {u}' for u, v in result_dict.items()], key=lambda x: int(x.split(' ')[-1]),
                         reverse=True)
    counter = 0
    tb = PrettyTable(['Count', 'Url', 'Code', 'Size'])
    tb.title = 'TOP 10 REQUESTS BY SIZE'
    for req in result_list:
        tb.add_row(req.split(' '))
        if counter == 9:
            break
        counter += 1
    if args.output:
        with open(args.output, 'a') as file:
            file.write(str(tb))
    else:
        print(tb)


def top10_400(_log):
    result_dict = dict(Counter([f'{i[0]} {i[1]} {i[2]} {i[3]}' for i in _log if re.match(r'^4\d+$', i[3])]))
    result_list = sorted([f'{v} {u}' for u, v in result_dict.items()], key=lambda x: int(x.split(' ')[0]),
                         reverse=True)
    counter = 0
    tb = PrettyTable(['Count', 'IP', 'Method', 'Url', 'Code'])
    tb.title = 'TOP 10 REQUESTS WITH CLIENT ERRORS'
    for req in result_list:
        tb.add_row(req.split(' '))
        if counter == 9:
            break
        counter += 1
    if args.output:
        with open(args.output, 'a') as file:
            file.write(str(tb))
    else:
        print(tb)


def top10_300(_log):
    result_dict = dict(Counter([f'{i[0]} {i[1]} {i[2]} {i[3]}' for i in _log if re.match(r'^3\d+$', i[3])]))
    result_list = sorted([f'{v} {u}' for u, v in result_dict.items()], key=lambda x: int(x.split(' ')[0]),
                         reverse=True)
    counter = 0
    tb = PrettyTable(['Count', 'IP', 'Method', 'Url', 'Code'])
    tb.title = 'TOP 10 REQUESTS WITH CLIENT ERRORS'
    for req in result_list:
        tb.add_row(req.split(' '))
        if counter == 9:
            break
        counter += 1
    if args.output:
        with open(args.output, 'a') as file:
            file.write(str(tb))
    else:
        print(tb)


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-c', action='store_true', help='display overall request count')
parser.add_argument('-t', action='store_true', help='display methods count')
parser.add_argument('-s', action='store_true', help='display top 10 requests by size')
parser.add_argument('-e', action='store_true', help='display top 10 requests with client errors')
parser.add_argument('-r', action='store_true', help='display top 10 requests with redirects')

parser.add_argument('--output', action='store', help='output file name in working directory')

parser.add_argument('path', type=str, help='path to file or directory')

if __name__ == '__main__':
    args = parser.parse_args()
    regx = re.compile(r'^(\d+.\d+.\d+.\d+) - - ([\s\S]+) (\"\w+ [\s\S]+ \w+/[\s\S]+\") (\d+) (\d+) ([\s\S]+)')
    paths = []

    if os.path.isfile(os.path.abspath(args.path)):
        paths.append(os.path.abspath(args.path))
    elif os.path.isdir(os.path.abspath(args.path)):
        paths = [os.path.join(os.path.abspath(args.path), i) for i in os.listdir(os.path.abspath(args.path))]
    else:
        print('Error: Incorrect path')
        exit(1)

    for path in paths:
        try:
            log, methods = process_file(path)
        except FileTypeException as exc:
            print(str(exc))
            continue

        if args.output:
            with open(args.output, 'w+') as file:
                file.write(f'\nFILE: {os.path.abspath(path)}\n')
        else:
            print(f'\nFILE: {os.path.abspath(path)}\n')
        if args.c:
            count_overall(log)
        if args.t:
            count_by_type(methods)
        if args.s:
            top10_by_size(log)
        if args.e:
            top10_400(log)
        if args.r:
            top10_300(log)
        if not args.c and not args.t and not args.s and not args.e and not args.r:
            count_overall(log)
            count_by_type(methods)
            top10_by_size(log)
            top10_400(log)
            top10_300(log)
