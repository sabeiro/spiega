---
title: "data storage"
author: Giovanni Marelli
date: 2019-07-02
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---
# data storage

Overview and usage of databases for data infrastructure purposes, `docker-compose` provided.

## volumes

It is always important to define external volumes connected with the database. Those volumes can be easily backed-up or synced on a cloud file system.

## relational

Usage of relational databases in different projects.

### postgres

Robust and stable database, used in different deployment as main database, great connections with BI tools and powerful geo spatial queries.

The useful files to create the container are under [postgres](https://github.com/sabeiro/sawmill/docker/postgres).

Once created the credential for the root user 
```bash
POSTGRES_USER=${DB_USER}
POSTGRES_PASSWORD=${DB_PASS}
POSTGRES_DB=api_ingest
```
The correspondent docker-compose is:

```yaml
services:
  db:
    image: postgres
    restart: unless-stopped
    env_file:
      - postgres/database.env
    ports:
      - '127.0.0.1:5432:5432'
    volumes:
      - db-data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/create_tables.sql
      - ./postgres/postgres.conf:/etc/postgresql/postgresql.conf
    #command: postgres -c config_file=/etc/postgresql/postgresql.conf
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "api_ingest"]
      interval: 5s
      retries: 5
    networks:
      - traefik-net
```

Connections to the database can be performed locally or with an orchestrator (swarm, kubernetes).

### mysql - mariadb

Mariadb is an optimal option for websites and lightweight applications, it's more performant and stable than mysql
[environment](https://github.com/sabeiro/sawmill/docker/webserver/mysql)

```bash
MARIADB_ROOT_PASSWORD=${DB_PASS_ROOT}
MARIADB_DATABASE=${DB_NAME}
MARIADB_USER=${DB_USER}
MARIADB_PASSWORD=${DB_PASS}
```
`docker-compose`

```yaml
services:
  mysql:
    #image: mysql
    image: mariadb
    restart: unless-stopped
    env_file:
      - mysql/mariadb.env
      #- mysql/database.env
    volumes:
      - ${HOME}/mysql-data:/var/lib/mysql
    networks:
      - webserver-net
```

### users

We can define each access user with such queries:

```sql
create user dash_ro with password '';
grant select on all tables in schema "public" to dash_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO dash_ro;
```

## presto



## document

### mongodb

## graph

### neo4j
