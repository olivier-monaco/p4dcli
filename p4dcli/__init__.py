import argparse
import p4d

from contextlib import closing


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--help', '-?', '-I', action='help',
                        help='Show this help message and exit')
    parser.add_argument('--host', '-h', help='Hostname', required=False,
                        default='localhost')
    parser.add_argument('--user', '-u', help='Username', required=False,
                        default='')
    parser.add_argument('--password', '-p', help='Password',
                        required=False, default='')
    parser.add_argument('base', help='Basename')
    return parser.parse_args()


def main():
    params = parse_args()

    cnx = p4d.connect(
        'host=' + params.host,
        user=params.user,
        password=params.password,
        database=params.base
    )

    while True:
        query = input("> ")
        if query == 'exit':
            break

        with closing(cnx.cursor()) as cur:
            try:
                cur.execute(query)
                _show_results(cur)
            except p4d.ProgrammingError as e:
                print('ERROR: {0}'.format(e.args[0].decode('utf-8')))


def _show_results(cur):
    columns = []
    lengths = []
    for column in cur.description:
        name = column[0].decode('utf-8')
        columns.append(name)
        lengths.append(len(name))

    rows = []
    for row in cur:
        values = []
        for index, value in enumerate(row):
            value = str(value)
            if len(value) > lengths[index]:
                lengths[index] = len(value)
            values.append(value)
        rows.append(values)

    sep = []
    fmt = []
    for length in lengths:
        sep.append('-' * length)
        fmt.append('{:' + str(length) + 's}')
    sep = '+-' + '-+-'.join(sep) + '-+'
    fmt = '| ' + ' | '.join(fmt) + ' |'

    print(fmt)
    print(sep)
    print(fmt.format(*columns))
    print(sep)
    for row in rows:
        print(fmt.format(*row))
    print(sep)
    print('{0} rows'.format(len(rows)))
    print()
