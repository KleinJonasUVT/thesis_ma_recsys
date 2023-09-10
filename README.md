# Thesis Marketing Analytics Recommendation Systems
## Running this project

### Using Docker

The easiest way to run this project is using Docker.

- [Install Docker](docs/install_docker.md) and clone this repository.
- Open the terminal at the repository's root directory and run the following commands: `docker build -t thesis_ma_recsys .` and `docker run -dp 127.0.0.1:5000:5000 thesis_ma_recsys`.
- Wait a bit for the website and API to be launched. If the process breaks, you likely haven't allocated enough memory (e.g., the built takes about 6 GB of memory)
- Once docker has been launched, you can access the website and API locally at these addresses:
    - API: `http://localhost:5000` (whereby localhost typically is `127.0.0.1`)
    - Front end: `http://localhost:5000`
- Press Ctrl + C in the terminal to quit.
