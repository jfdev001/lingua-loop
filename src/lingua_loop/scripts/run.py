import threading
import webbrowser

import uvicorn


def run():
    """
    TODO: Starting on port is fragile. Dynamically assign like in jupyter-server
    or otherwise.

    Reference: https://github.com/Kludex/uvicorn/issues/761#issuecomment-1287679527
    """
    host = "127.0.0.1"
    free_port = 49152
    threading.Timer(2.0, lambda: webbrowser.open(f"{host}:{free_port}")).start()
    uvicorn.run("lingua_loop.main:app", host=host, port=free_port, reload=True)


if __name__ == "__main__":
    run()
