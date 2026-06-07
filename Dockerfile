FROM python:3.12-slim

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN uv sync --no-default-groups

EXPOSE 49152

ENV PATH="/app/.venv/bin:$PATH"
CMD ["lingua-loop"]
