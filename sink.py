import logging
import itertools
import time

import zmq

PULL_PORT = 13132
PULL_ADDR = "tcp://*:{}".format(PULL_PORT)

logging.basicConfig(level=logging.INFO)

def run_sink(pull):
    while True:
        info  = pull.recv()
        logging.info("Recv")

def main():
    context = zmq.Context()
    pull = context.socket(zmq.PULL)
    pull.bind(PULL_ADDR)
    run_sink(pull)
    pull.close()
    context.term()

if __name__ == "__main__":
    main()
