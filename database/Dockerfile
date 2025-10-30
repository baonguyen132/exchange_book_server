FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=exchange_book
ENV MYSQL_USER=exchange_user
ENV MYSQL_PASSWORD=exchange_pass

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306