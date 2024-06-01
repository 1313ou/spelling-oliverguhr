#!/usr/bin/python3

import argparse
import sys
import sqlite3
from tqdm.auto import tqdm

import _oliverguhr

sql = "SELECT sampleid, sample FROM samples"
sqlcount = "SELECT COUNT(*) FROM samples"


def check_oliverguhr(input_text, id):
    corrections = _oliverguhr.spell_check(input_text, id)
    if corrections:
        print(f"{id}\t{input_text}\t{corrections}")


def count(conn, resume):
    cursor = conn.cursor()
    sql2 = sqlcount
    if resume:
        sql2 += f" WHERE sampleid >= {resume}"
    cursor.execute(sql2)
    return cursor.fetchone()[0]


def read(file, resume, checkf):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    sql2 = sql
    if resume:
        sql2 += f" WHERE sampleid >= {resume}"
    cursor.execute(sql2)
    n = count(conn, resume)
    pb = tqdm(total=n)
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        rowid = row[0]
        sample = row[1]
        checkf(sample, rowid)
        pb.update(1)
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="scans the samples from sqlite file")
    parser.add_argument('database', type=str, help='database')
    parser.add_argument('--resume', type=int, help='row to resume from')
    args = parser.parse_args()
    read(args.database, args.resume, check_oliverguhr)


if __name__ == '__main__':
    main()
