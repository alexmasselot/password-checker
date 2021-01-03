FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update

COPY ./components/api/app /app
COPY ./components/frontend/dist/* /app/static/

ENV LISTEN_PORT=8000
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]


