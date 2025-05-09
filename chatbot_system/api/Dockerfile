FROM python:3.8.6-slim

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

# Install compatible versions
RUN python -m pip install -r requirements.txt

COPY fav_foods/ fav_foods/
COPY agent/ agent/
COPY brain_agent.py brain_agent.py
COPY main.py main.py


ENTRYPOINT [ "python", "main.py"]