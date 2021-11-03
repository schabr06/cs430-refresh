"""Simple client program"""
import argparse
import logging
import socket

HOST = "localhost"
PORT = 4300


def format(message: list) -> bytes:
    """Convert (encode) the message to bytes"""
    return f"Hello, my name is {' '.join(message)}".encode()


def parse(data: bytes) -> str:
    """Convert (decode) bytes to a string"""
    return data.decode()


def client_loop(name: str):
    print("The client has started")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        logging.info(f"Connecting to {HOST}:{PORT}")
        sock.connect((HOST, PORT))
        logging.info(f"Connected to {HOST}:{PORT}")
        logging.info("Formatting data")
        data_out = format(name)
        logging.info("Sending data")
        sock.sendall(data_out)
        logging.info("Receiving data")
        data_in = sock.recv(1024)
        logging.info("Parsing data")
        message = parse(data_in)
        print(f"Server responded: {message}")
    print("The client has finished")


def main():
    arg_parser = argparse.ArgumentParser(description="Enable debugging")
    arg_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable logging.DEBUG mode"
    )
    arg_parser.add_argument(
        "name", type=str, nargs="+", help="Enter message to send"
    )
    args = arg_parser.parse_args()
    logger = logging.getLogger("root")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.WARNING)
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logger.level)
    name = args.name
    client_loop(name)


if __name__ == "__main__":
    main()
