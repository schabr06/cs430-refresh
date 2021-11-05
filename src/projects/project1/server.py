#!/usr/bin/env python3
"""Simple server program"""
import argparse
import logging
import socket
from csv import DictReader
from typing import Tuple


HOST = "127.0.0.1"
PORT = 4300


def read_file(filename: str) -> Tuple[dict, int]:
    """Read the world countries and their capitals from the file
    Return the tuple of (dictionary, count) where
    `dictionary` is a map {country:capital} and
    `count` is the number of countries in the world
    Make sure not to count United States of America and USA as two different countries
    """
    with open(filename, newline='') as csvfile:
        dictionary = {}
        reader = DictReader(csvfile, fieldnames=('Country', 'Capital'), dialect='excel', delimiter=(';'))
        count = 0
        for row in reader:
            if row['Country'] =="Côte D'Ivoire, Ivory Coast":
                dictionary["Côte D'Ivoire"] = row['Capital']
                dictionary["Ivory Coast"] = row['Capital']
                count += 1
            elif row['Country'] == "Czechia, Czech Republic":
                dictionary["Czechia"] = row['Capital']
                dictionary["Czech Republic"] = row['Capital']
                count += 1
            elif row['Country'] == "United Arab Emirates, UAE":
                dictionary["United Arab Emirates"] = row['Capital']
                dictionary["UAE"] = row['Capital']
                count += 1
            elif row['Country'] == "United Kingdom, UK":
                dictionary["United Kingdom"] = row['Capital']
                dictionary["UK"] = row['Capital']
                count += 1
            elif row['Country'] == "United States of America, USA":
                dictionary["United States of America"] = row['Capital']
                dictionary["USA"] = row['Capital']
                count += 1
            elif row['Country'] == "Country":
                pass
            else:
                dictionary[row['Country']] = row['Capital']
                count += 1
        tup = (dictionary, count)
        return tup


def find_capital(world: dict, country: str) -> str:
    """Return the capital of a country if it exists
    Return *No such country* otherwise
    """
    capital = world.get(country)
    if capital == None:
        return "No such country."
    else:
        return capital

def format(message: str) -> bytes:
    """Convert (encode) the message to bytes"""
    return message.encode()


def parse(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    return data.decode()


def server_loop(world: dict):
    print("The server has started")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        while True:
            msg, addr = sock.recvfrom(2048)
            msg = parse(msg)
            if msg == 'BYE':
                break
            else:
                respone = format(find_capital(world, msg))
                sock.sendto(respone, addr)
    sock.close()
    print("The server has finished")


def main():
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument("-f", "--file", type=str, help="File name")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
    )
    args = arg_parser.parse_args()
    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    world, _ = read_file(args.file)
    server_loop(world)


if __name__ == "__main__":
    main()
