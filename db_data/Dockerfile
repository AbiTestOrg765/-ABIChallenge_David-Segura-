FROM postgres:16.4


## Docker file for postgres DB
ENV POSTGRES_USER=david
ENV POSTGRES_PASSWORD=david123
ENV POSTGRES_DB=appMl

# Creates postgres db required tables
COPY init.sql /docker-entrypoint-initdb.d/

# Exposes database to port 5432
EXPOSE 5432