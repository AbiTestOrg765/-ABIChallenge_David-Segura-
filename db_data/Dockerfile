FROM postgres:16.4


## Had issues with running inside docker compose file so decided to create a db with his own dockerfile
ENV POSTGRES_USER=david
ENV POSTGRES_PASSWORD=david123
ENV POSTGRES_DB=appMl

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432