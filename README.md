![example workflow](https://github.com/muzaparoff/counter-service/actions/workflows/main.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# Counter Service

The Counter Service is a simple web application that maintains a counter of the number of POST requests it has served and displays it on every GET request. This README provides an overview of the service and instructions on how to set it up and use it.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Running Locally](#running-locally)
  - [Deploying on a Server](#deploying-on-a-server)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 installed
- Docker and Docker Compose (for containerized deployment)
- Internet access to download dependencies

### Running Locally

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/muzaparoff/counter-service.git
   cd counter-service
   ```

2. Start the service using Docker Compose:

   ```shell
   docker-compose up -d
   ```

3. Open your web browser and navigate to `http://localhost:5000` to see the Counter Service in action.

### Connecting to RabbitMQ

To connect to RabbitMQ running on localhost, use the following command in your terminal:

```shell
docker run -d --hostname my-rabbit --name some-rabbit rabbitmq:3
```

You can then access the RabbitMQ management interface by navigating to `http://localhost:15672` in your web browser. The default username and password are both `guest`.

### Usage

The Counter Service is a simple web service with the following behavior:

- A GET request to the root URL (/) returns a web page displaying the current count of POST requests served.
- A POST request to the root URL (/) increments the count.

You can use web browsers, HTTP clients (e.g., curl, Postman), or scripts to interact with the service.

### API Endpoints

- GET /: Returns a web page displaying the current count.
- POST /: Increments the count and returns the updated count.
- GET /health: Returns a status code of 200 (OK), it prints "Health check passed" to the workflow logs.

### Testing

To run tests for the Counter Service, use the following command:

1. Navigate to the project directory:

    ```shell
    cd counter-service
    ```

2. Install the necessary dependencies:

    ```shell
    pip install -r requirements.txt
    ```

3. Run the tests:

    ```shell
    python test_counter_service.py
    ```

### Contributing

Contributions are welcome! If you would like to contribute to this project, please follow the standard guidelines for open-source contributions.

### License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.