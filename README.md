# Project README

## Project Overview

This project is designed to use Ollama, a powerful tool for various functionalities including embeddings. It combines a backend server powered by Uvicorn and a frontend served via `index.html`. Follow the instructions below to set up and run the project.

## Prerequisites

- Python 3.x
- Pip (Python package installer)
- Virtual environment tool (`venv`)
- Ollama CLI installed and configured

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine. Open a terminal and run:

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Set Up Virtual Environment

Create a virtual environment using Python's `venv` module:

```sh
python -m venv venv
```

Activate the virtual environment:

- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages listed in `requirements.txt`:

```sh
pip install -r requirements.txt
```

### 4. Pull Ollama Model

Pull the `mxbai-embed-large` model from Ollama:

```sh
ollama pull mxbai-embed-large
```

After running the above command, restart your terminal and reactivate the virtual environment:

- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 5. Install Additional Packages

Install Uvicorn, an ASGI server implementation:

```sh
pip install uvicorn
```

Install the Langchain Community package:

```sh
pip install langchain-community
```

## Running the Application

Start the Uvicorn server:

```sh
uvicorn app:app --reload
```
This command will start the backend server and enable hot-reloading for development purposes.

Replace <YOUR-OPENAI-KEY> with your own secret key in .env file.
Replace <YOUR REPLICATE API KEY> with your own replicate secret key in chatbot.py file

## Frontend

The frontend of the application is served by `index.html`. Ensure this file is in the appropriate directory as expected by your backend configuration.

## Conclusion

Your application should now be up and running. You can access it via the address provided by Uvicorn, typically `http://127.0.0.1:8000`.

For further details on usage and contributing, please refer to the documentation or contact the project maintainer.

---

Feel free to reach out if you encounter any issues or have any questions!
