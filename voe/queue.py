import logging
import itertools
import time

import zmq

from producer import get_tasks

PUSH_PORT = 1313
SYNC_PORT = 13131

PUSH_ADDR = "tcp://*:{}".format(PUSH_PORT)
SYNC_ADDR = "tcp://*:{}".format(SYNC_PORT)

logging.basicConfig(level=logging.INFO)

def run(sync, push, tasks):
    for task in itertools.cycle(tasks):
        ready = sync.recv()

        # pra garantir que o primeiro cliente não receba as 2 primeiras
        # mensagens em seguida permitindo a distribuição igual entre todos
        # os nós desde a primeira mensagem
        time.sleep(0.3)

        logging.info(task)
        push.send(task)

def main():
    tasks = get_tasks()
    context = zmq.Context()

    push = context.socket(zmq.PUSH)
    sync = context.socket(zmq.DEALER)

    push.bind(PUSH_ADDR)
    sync.bind(SYNC_ADDR)

    run(sync, push, tasks)

    sync.close()
    push.close()

    context.term()

if __name__ == "__main__":
    main()
