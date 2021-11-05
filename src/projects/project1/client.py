#!/usr/bin/env python3
"""Simple client program"""
import argparse
import logging
import socket

HOST = "localhost"
PORT = 4300


def format(message: list) -> bytes:
    """Convert (encode) the message to bytes"""
    return ''.join(message).encode()


def parse(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    return data.decode()


def read_user_input() -> str:
    """Read user input from the console and return it"""
    user_innput: str = input("Enter a country name or BYE to exit: ")
    return user_innput


def client_loop():
    print("The client has started")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        while True:
            user_input = read_user_input()
            sock.sendto(format(user_input), ((HOST, PORT)))
            if user_input == 'BYE':
                break
            response, _ = sock.recvfrom(2048)
            print(f"Received: {parse(response)}")
    sock.close()
    print("The client has finished")


def main():
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
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
    client_loop()


if __name__ == "__main__":
    main()
