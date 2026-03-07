import uvicorn


def run():
    uvicorn.run(
        "lingua_loop.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    run()
