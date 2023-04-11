FROM mysql/mysql-server
ENV MYSQL_ROOT_PASSWORD=root
ADD create_db.sql /docker-entrypoint-initdb.d
EXPOSE 3306