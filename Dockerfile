FROM mysql:8.0
# Copy the initialization script to create the database and tables
COPY ./backend/db/create_db.sql /docker-entrypoint-initdb.d/create_db.sql