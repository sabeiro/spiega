---
title: golang
author: Giovanni Marelli
date: 2019-09-12
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
id: golang
category: #tech
roam_refs: golang 
roam_aliases: ["golang"]
output: 
	md_document:
		variant: markdown_strict+backtick_code_blocks+autolink_bare_uris+markdown_github
---


# golang

Go is a language pretty efficient to build backends. In some projects I decided to use it for building fast and reliable backends

# middleware

Here's a breakdown of the main features of each Go project:

### `.htpasswd.go`:
- **Purpose**: Manages HTTP Basic Authentication in Nginx.
- **Format**: Each line contains a username and a hashed password using an MD5 hashing algorithm, prefixed by `$apr1$`.
- **Example**: The file contains the hashed password for "ws".

### `modules.go` in the `logspout` directory:
- **Purpose**: Provides configuration and installation of components required for Logstash support using Logspout.
- **Components**:
  - Healthcheck package: Monitors the status of Logspout.
  - TCP and UDP transport packages: Enable sending logs to various destinations.
  - Logstash adapter: Routes logs to Logstash instances.

### Web Server Configuration:
- **Features**:
  - Handles API endpoints using Gorilla Mux.
  - Supports HTTP methods like POST, GET, PUT, and DELETE.
  - Static content serving from `/apidocs/` and `/static/`.
  - Error handling through response functions (`respondWithError` and `respondWithJSON`).
  - Defines routes for various functionalities including index pages, page retrieval, authentication, CRUD operations, and Swagger documentation access.

### API Management:
- **Package**: `go_ingest`
- **Features**:
  - Initializes a database connection using environment variables.
  - Ensures the `products` table exists in the database.
  - Deletes all entries from the `products` table before running tests and reinitializes the sequence for new IDs.
  - Provides helper functions (`ensureTableExists`, `clearTable`) to manage table creation and data cleaning.
  - Uses Gorilla Mux for routing with test functions that cover scenarios such as empty tables, non-existent products, product creation, retrieval, updating, and deletion.

### Authentication:
- **Functions**:
  - `userpassword`: Maps usernames to hashed passwords.
  - `generateJWT`: Generates a JWT signed with HS256 using a secret key.
  - `authenticateRequest`: Validates user credentials based on Base64-encoded headers.
  - `authenticateJWT`: Validates JWT tokens sent in the request.

### Swagger Documentation:
- **Package**: `docs`
- **Features**:
  - Uses Swag to generate a Swagger documentation template for the API.
  - Registers Swagger information with Swag's registration system, which generates actual Swagger documentation when the application starts.
  - Provides embedded files (`embed` package) to access static files without manual loading from the filesystem.

### Database Operations:
- **Package**: `main`
- **Features**:
  - Initializes an App struct using environment variables for database connection parameters.
  - Runs on port 5006 and handles operations like querying, updating, deleting, and creating entries in a database using the SQL package.

These projects demonstrate various aspects of Go programming, including authentication, web server configuration, API management, and document generation. Each project provides a clear structure for handling specific functionalities within a larger application environment.

