# Unibrowser Backend Scapers
Data acquisition scripts to assist with populating the Unibrowser database with useful university information

## For Developers
The scripts are developed using **Python version 3.6**. Unit tests are done using `pytest`. The best way to develop this project is to use a virtual python environment and install the necessary dependencies, modifying the `requirements.txt` file as needed to add new dependencies.

### Dependency Installation
To install the necessary dependencies on your system, the following pre-requisites needs to be met:
- `python-dev` and `python3-dev` system packages are installed (used when compiling certain library dependencies)

```text
> pip install -r requirements.txt
> python setup.py
```

### Configuration
Configuration for the production environment, test environment, and development environment now live inside of the `config/` directory as the following:
- `prod.py`: production configuration
- `test.py`: test environment configuration
- `user.py`: (not checked in, ignored) developer configuration specific to each user. SHOULD NOT BE CHECKED IN.

The loaded configuration is dependent upon the `UNI_MODE` environment variable. The following table describes the behavior of configuration based on this variable:
| Environment Variale | Value | Effect |
|---|---|---|
| `UNI_MODE` | `production` | Load the `prod.py` file contents |
| `UNI_MODE` | `test` | Load the `test.py` file contents |
| `UNI_MODE` | empty or `user` | Load the `user.py` file contents |

The loading logic is handled inside of the `config/__init__.py` file. Whenever new configuration is added, make sure to add it to both the `prod.py` and `test.py` files, since each is independent of the other. To use the configuration values, simply import the `config` module as follows

```python
from config import DATABASE_CONFIG # or whichever config you need to load
...
```

### Running the Scripts
All scripts should be run from the root of the repository. For example, if you want to run the free food data extractor, run `python scraping/tweetextractor.py`.

### Unit Tests
Unit testing is completed using `pytest`. To run the unit tests, simply type the following from the root of the repository:

```text
> pytest
```

This will run the tests and generate a report of the results. The `pytest.ini` file at the root of the repo defines configuratio for the `pytest` module.
