#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import argparse


def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-f', '--file')
 
    return parser


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args()
    try:
        file = namespace.file
        with open(file, 'r') as f:
            read_data = f.read()
            data = read_data.split("\n")
            i = 0
            for line in data:
                line = ' '.join(line.split())
                line = line.split(' ')
                # dump = line.split(' ')
                print "('%s', '%s'), " % (line[0], line[0]),
        f.close()
    except:
        print ("введи имя файла через -f или --file")