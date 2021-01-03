FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update

COPY ./components/api/app /app
COPY ./components/frontend/dist/. /app/static/

ENV STATIC_INDEX 1

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]


