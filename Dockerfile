FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update

COPY ./components/api/app /app
COPY ./components/frontend/dist/* /app/static/


