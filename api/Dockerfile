FROM python:3.9-slim

COPY requirements/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app/

COPY ./cnab/ .

CMD ["gunicorn", "-b", ":8000", "cnab.wsgi:application"]
