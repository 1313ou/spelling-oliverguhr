#!/usr/bin/python3

import argparse


def process_text(text, id):
    print(f"{id}\t{text}")


def read_line(line, checkf):
    fields = line.split('\t')
    checkf(fields[1], fields[0])


def read_file(file, resume, linef, checkf):
    with open(file) as fp:
        for line in fp:
            linef(line.strip(), checkf)


def get_processing(name):
    return globals()[name] if name else process_text


def main():
    parser = argparse.ArgumentParser(description="scans the samples from sqlite file")
    parser.add_argument('file', type=str, help='text')
    parser.add_argument('--resume', type=int, help='line to resume from')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    read_file(args.file, args.resume, read_line, get_processing(args.processing))


if __name__ == '__main__':
    main()
