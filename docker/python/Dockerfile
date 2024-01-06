FROM python:3.11-slim as Builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk \
    tk-dev \
    libtk8.6 

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt
RUN pip 

COPY . /app


FROM python:3.11-slim

WORKDIR /app

COPY --from=Builder /app/ .
COPY --from=Builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["python", "main.py"]