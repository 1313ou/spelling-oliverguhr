#!/usr/bin/python3

import argparse
import sqlite3

import _oliverguhr

sql = "SELECT sampleid, sample FROM samples"


def check_oliverguhr(input_text, id):
    if not _oliverguhr.spell_check(input_text, id):
        print(f"{id}\r{input_text}")


def read(file, resume, checkf):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    sql2 = sql
    if resume:
        sql2 += f" WHERE sampleid >= {resume}"
    cursor.execute(sql2)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        rowid = row[0]
        sample = row[1]
        checkf(sample, rowid)
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="scans the samples from sqlite file")
    parser.add_argument('database', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    args = parser.parse_args()
    read(args.database, args.resume, check_oliverguhr)


if __name__ == '__main__':
    main()
