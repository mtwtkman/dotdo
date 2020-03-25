FROM python:alpine
RUN apk add --update gcc libffi-dev musl-dev openssl-dev
RUN pip install poetry
RUN mkdir /app
WORKDIR /app
COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY dotdo.py dotdo.py
RUN poetry install
COPY example.py example.py
COPY example.ini example.ini
EXPOSE 55301 55301
CMD ["poetry", "run", "pserve", "example.ini"]