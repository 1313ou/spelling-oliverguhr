#!/usr/bin/python3

import argparse
import sqlite3
from tqdm.auto import tqdm

import _oliverguhr

sql_definitions = "SELECT synsetid, definition FROM synsets"
sql_definitions_count = "SELECT COUNT(*) FROM synsets"


def count(conn, resume):
    cursor = conn.cursor()
    sql2 = build_sql(sql_definitions_count, resume)
    cursor.execute(sql2)
    return cursor.fetchone()[0]


def build_sql(sql, resume):
    return sql + f" WHERE synsetid >= {resume}" if resume else sql


def read(file, resume, checkf):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    sql2 = build_sql(sql_definitions, resume)
    cursor.execute(sql2)
    n = count(conn, resume)
    pb = tqdm(total=n)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        rowid = row[0]
        definition = row[1]
        checkf(definition, rowid)
        pb.update(1)
    conn.close()


def get_processing(name):
    return globals()[name] if name else _oliverguhr.spell_check_print


def main():
    parser = argparse.ArgumentParser(description="scans the definitions from sqlite file")
    parser.add_argument('database', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    read(args.database, args.resume, processing)


if __name__ == '__main__':
    main()
