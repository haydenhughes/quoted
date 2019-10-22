#!/usr/bin/python3

"""A simple script to more easily create quotes with the quoted api."""

import requests
import argparse
import json

parser = argparse.ArgumentParser(
    description='A simple script to more easily create requests for the quoted api.')
parser.add_argument('server', help='url for the location of the server')
parser.add_argument('file', help='location of json file to equest from')

args = parser.parse_args()

with open(args.file) as fp:
    r = requests.post(f'{args.server}/api/v1.0/quotes', json=json.load(fp))
    print(r.text)
