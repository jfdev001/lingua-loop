import threading
import webbrowser
from os import mkdir
from os.path import exists

import uvicorn

from lingua_loop.constants import DATABASE_DIR


def run():
    """
    TODO: Starting on port is fragile. Dynamically assign like in jupyter-server
    or otherwise.

    Reference: https://github.com/Kludex/uvicorn/issues/761#issuecomment-1287679527
    """

    if not exists(DATABASE_DIR):
        print(f"Making {DATABASE_DIR}")
        mkdir(DATABASE_DIR)

    host = "127.0.0.1"
    free_port = 49152
    threading.Timer(
        2.0, lambda: webbrowser.open(f"http://{host}:{free_port}")
    ).start()
    uvicorn.run("lingua_loop.main:app", host=host, port=free_port, reload=True)


if __name__ == "__main__":
    run()
