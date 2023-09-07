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
   docker-compose up -d

### Testing
To run tests for the Counter Service, use the following command:

    shell
    Copy code
    python test_counter_service.py
    Contributing
    Contributions are welcome! If you would like to contribute to this project, please follow the standard guidelines for open-source contributions.

License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.