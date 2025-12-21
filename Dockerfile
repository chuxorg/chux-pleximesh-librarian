FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    LIBRARIAN_PORT=8000 \
    LIBRARIAN_ARTIFACT_ROOT=/data/librarian

COPY server.py README.md CONTRIBUTING.md /app/

EXPOSE 8000

CMD ["python", "server.py"]
