import argparse
import os
import re
from prettytable import PrettyTable
import pymysql


class Connection:
    def __init__(self):
        self.connection = pymysql.connect(
            host=args.host,
            port=int(args.port),
            user=args.user,
            password=args.password,
            db=None,
            charset='utf8',
            autocommit=True
        )
        self.flag = False

        self.connection.query(f'CREATE DATABASE if not exists {args.db}')
        self.connection.query(f'USE {args.db}')

    def table_init(self, _path):
        self.connection.query(
            f"""CREATE TABLE if not exists `{_path[max(0, len(_path)) - 64:]}`( 
            `ip` text NOT NULL,
            `method` varchar(10) NOT NULL,
            `url` text NOT NULL,
            `status_code` smallint(3) NOT NULL,
            `size` int NOT NULL) CHARSET=utf8
        """)

    def check(self, _path):
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        for row in cursor.fetchall():
            if _path[max(0, len(_path)) - 64:] in row:
                return True

        return False

    def count_overall(self, _path):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM `{_path[max(0, len(_path)) - 64:]}`")
        tb = PrettyTable(['OVERALL REQUESTS COUNT'])
        for row in cursor.fetchall():
            tb.add_row([row[0]])
        print(tb)

    def count_by_type(self, _path):
        cursor = self.connection.cursor()
        cursor.execute(f"select method, count(*) from `{_path[max(0, len(_path)) - 64:]}` group by method")
        tb = PrettyTable(['Method', 'Count'])
        tb.title = 'REQUESTS COUNT BY TYPE'
        for row in cursor.fetchall():
            tb.add_row([row[0], row[1]])
        print(tb)

    def top10_by_size(self, _path):
        cursor = self.connection.cursor()
        cursor.execute(f"""
            select count(*), url, status_code, size from `{_path[max(0, len(_path)) - 64:]}`
            group by url, status_code, size
            order by size desc
            limit 10
        """)
        tb = PrettyTable(['Count', 'Url', 'Code', 'Size'])
        tb.title = 'TOP 10 REQUESTS BY SIZE'
        for row in cursor.fetchall():
            tb.add_row([row[0], row[1], row[2], row[3]])
        print(tb)

    def top10_400(self, _path):
        cursor = self.connection.cursor()
        cursor.execute(f"""
            select count(*), ip, method, url, status_code from `{_path[max(0, len(_path)) - 64:]}`
            where status_code like "4%"
            group by ip, method, url, status_code
            order by count(*) desc
            limit 10
        """)
        tb = PrettyTable(['Count', 'IP', 'Method', 'Url', 'Code'])
        tb.title = 'TOP 10 REQUESTS WITH CLIENT ERRORS'
        for row in cursor.fetchall():
            tb.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(tb)

    def top10_300(self, _path):
        cursor = self.connection.cursor()
        cursor.execute(f"""
            select count(*), ip, method, url, status_code from `{_path[max(0, len(_path)) - 64:]}`
            where status_code like "3%"
            group by ip, method, url, status_code
            order by count(*) desc
            limit 10
        """)
        tb = PrettyTable(['Count', 'IP', 'Method', 'Url', 'Code'])
        tb.title = 'TOP 10 REQUESTS WITH CLIENT ERRORS'
        for row in cursor.fetchall():
            tb.add_row([row[0], row[1], row[2], row[3], row[4]])
        print(tb)


class FileTypeException(Exception):
    pass


class TableExistsException(Exception):
    pass


def log_check(_line, _regx):
    return _regx.match(_line)


def parse_line(_line):
    line_list = _line.replace('"', '').replace('[', '').replace(']', '').split(' ')[0:10]
    return [line_list[0], line_list[5], line_list[6], line_list[8], line_list[9]]


def process_file_to_db(filename, _connection):
    with open(filename) as file:
        if not log_check(file.readline(), regx):
            raise FileTypeException(f'{filename} is not a nginx log')
        if connection.check(filename):
            raise TableExistsException(f'{filename} is already in db')
        else:
            connection.table_init(filename)
        file.seek(0)
        for line in file.readlines():
            request = parse_line(line)
            _connection.connection.query(f"""
                INSERT INTO `{filename[max(0, len(filename)) - 64:]}`
                VALUES ('{request[0]}', '{request[1]}', '{request[2]}', '{request[3]}', '{request[4]}')
            """)


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-c', action='store_true', help='display overall request count')
parser.add_argument('-t', action='store_true', help='display methods count')
parser.add_argument('-s', action='store_true', help='display top 10 requests by size')
parser.add_argument('-e', action='store_true', help='display top 10 requests with client errors')
parser.add_argument('-r', action='store_true', help='display top 10 requests with redirects')

parser.add_argument('--host', type=str, action='store', help='connection hostname')
parser.add_argument('--port', type=str, action='store', help='connection port')
parser.add_argument('--user', type=str, action='store', help='connection username')
parser.add_argument('--password', type=str, action='store', help='connection password')
parser.add_argument('--db', type=str, action='store', help='connection password')

parser.add_argument('path', type=str, help='path to file or directory')

if __name__ == '__main__':
    args = parser.parse_args()
    regx = re.compile(r'^(\d+.\d+.\d+.\d+) - - ([\s\S]+) (\"\w+ [\s\S]+ \w+/[\s\S]+\") (\d+) (\d+) ([\s\S]+)')
    paths = []

    if not args.host and not args.port and not args.user and not args.password and not args.db:
        print('Missing required arguments')
        exit(1)

    if os.path.isfile(os.path.abspath(args.path)):
        paths.append(os.path.abspath(args.path))
    elif os.path.isdir(os.path.abspath(args.path)):
        paths = [os.path.join(os.path.abspath(args.path), i) for i in os.listdir(os.path.abspath(args.path))]
    else:
        print('Error: Incorrect path')
        exit(1)

    connection = Connection()

    for path in paths:
        try:
            print(f'Putting {path} in db')
            process_file_to_db(path, connection)
        except FileTypeException as exc:
            print(str(exc))
            continue
        except TableExistsException as exc:
            print(str(exc))

        print(f"\nFILE: {path}\n")

        if args.c:
            connection.count_overall(path)
        if args.t:
            connection.count_by_type(path)
        if args.s:
            connection.top10_by_size(path)
        if args.e:
            connection.top10_400(path)
        if args.r:
            connection.top10_300(path)
        if not args.c and not args.t and not args.s and not args.e and not args.r:
            connection.count_overall(path)
            connection.count_by_type(path)
            connection.top10_by_size(path)
            connection.top10_400(path)
            connection.top10_300(path)
