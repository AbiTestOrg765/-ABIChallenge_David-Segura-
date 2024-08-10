FROM postgres:latest

ENV POSTGRES_USER=david
ENV POSTGRES_PASSWORD=david123
ENV POSTGRES_DB=appMl

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432