# Simple HTTP Server
=====================

A basic HTTP server written in Python using the `socket` library.

## Main Goal

The main goal of this repository is to create a simple HTTP server that can serve static files, including HTML, CSS, and images.

## Features

* Listens for incoming connections on a specified port
* Serves files from a designated document root directory
* Supports HTTP GET and HEAD requests

## Usage

1. Clone the repository and navigate to the project directory.
2. Run the server using `python httpd.py`.
3. Open a web browser and navigate to `http://localhost:8080` to access the server.

## Configuration

* The server listens on port 8080 by default. You can change this by modifying the `PORT` variable in `httpd.py`.
* The document root directory is set to `./www` by default. You can change this by modifying the `DOCUMENT_ROOT` variable in `httpd.py`.

## Dependencies

This project uses Poetry to manage dependencies. To install the required dependencies, follow these steps:

### Install Poetry

If you haven't already, install Poetry using the following command:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install Dependencies

Once Poetry is installed, navigate to the project directory and run the following command:
```bash
poetry install
```

### Testing
To test the server, navigate to http://localhost:8080/httptest/wikipedia_russia.html in your web browser. 
This should correctly load the static Wikipedia page, including all CSS and images.