# voxus-challenge
Voxus Challenge I - Sunrise and Sunset information based in latitude and longitude with RestAPI interface.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Docker**: Install Docker on your system. You can download it [here](https://www.docker.com/get-started).

## Getting Started

To get this project up and running, follow these steps:

1. Clone this repository:

   ```bash
   git clone <repository-url>
   cd project-directory
   ```
2. Create a .env file and set environment variables that your project requires. Refer to the .env.dev file for examples or create your self .env file for your working setup.
   ```bash
   cat .env.dev > .env # for development mode
   ```

3. Build and start the Docker containers of docker-compose.yaml:

   ```bash
   docker compose --env-file .env up -d
   ```

3. Swagger Endpoint documentation based in Postman can be found at: https://github.com/MichaelDeMattos/voxus-challenge/docs/

## Tech Stack

- **Python**: Python is a high-level, interpreted, script, imperative, object-oriented, functional, dynamically-typed, and strongly-typed programming language.
    - **pytest**: Pytest is a Python testing framework that originated from the PyPy project.
    - **Flask**: Flask is an HTTP framework for Python, simplifying API development and web applications.
    - **Pydantic**: Pydantic is the most widely used data validation library for Python.
    - **AIOHTTP**: Asynchronous HTTP Client/Server for asyncio and Python.
    - **uWSGI**: WSGI HTTP Server for UNIX

- **Redis**: Redis is an in-memory key-value store known for its low-latency and high-performance data retrieval.

- **Nginx**: Nginx is a high-performance, open-source HTTP server, proxy server, and reverse proxy server that can also function as a load balancer.
- **Docker**: Docker is an open platform for developing, shipping, and running applications.

**Connect with Me:**

- **GitHub**: [MichaelDeMattos](https://github.com/MichaelDeMattos/)

- **LinkedIn**: [Michael Ortiz](https://www.linkedin.com/in/michael-ortiz-57690a17a/)
