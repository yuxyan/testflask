#
FROM python:3.12

#
COPY ./requirements.txt /requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

#
COPY ./.env /.env

#
COPY ./app /app

#
COPY ./alembic.ini /alembic.ini

#
COPY ./alembic /alembic

#
EXPOSE 5000

#
WORKDIR /app

#
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]