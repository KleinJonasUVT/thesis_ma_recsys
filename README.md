# Thesis Marketing Analytics Recommendation Systems
## Running this project

### Using Docker

The easiest way to run this project is using Docker.

- [Install Docker](docs/install_docker.md) and clone this repository.
- Open the terminal at the repository's root directory and run the following command: `docker build -t thesis_ma_recsys .`
- Ask the developers of this repository for access to the connection string to the database in which all credentials are stored and run the following command: `docker run -e DB_CONNECTION_STRING="actual_connection_string" -dp 127.0.0.1:5000:5000 thesis_ma_recsys`. Replace `actual_connection_string` with the actual connection string you received from the developers.
- Wait a bit for the website and API to be launched. If the process breaks, you likely haven't allocated enough memory (e.g., the built takes about 6 GB of memory)
- Once docker has been launched, you can access the website at these addresses:
    - `[http://localhost:5000](http://127.0.0.1:5000)`
    - `[http://localhost:5000](http://172.17.0.2:5000)`
- Press Ctrl + C in the terminal to quit.
