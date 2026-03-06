import uvicorn


def run():
    uvicorn.run(
        "lingua_loop.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )


if __name__ == "__main__":
    run()
