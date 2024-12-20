# Digital Rule Engine API (Unofficial)

## 1. Overview
The `Digital Rule Engine API` is a scheduled rules engine designed to evaluate and process rules, including campaign flags and other criteria, stored in a local PostgreSQL database. This data is sourced from ADL GAM Datastores and local Data Ponds.

## 2. Requirements and Configurations
### Requirements

###### Python

1. Download and Install [Python](https://www.python.org/downloads/)

###### PostgreSQL
1. Download and Install [PostgreSQL](https://www.postgresql.org/download/)

###### IDE
1. Download and install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/?section=windows) 

###### IDE Plugins
To install a plugin in IntelliJ IDEA or PyCharm go to Settings > Plugins > Marketplace > Search for the plugin name and click Install.
1. Add the plugin [Python Community Edition](https://plugins.jetbrains.com/plugin/7322-python-community-edition)
2. Add the plugin [Pylint](https://plugins.jetbrains.com/plugin/11084-pylint) (Optional, if you want Pylint highlighting)

___
### Configurations
###### Pylint Plugin
1. Add the pylint package (only to you venv, don't add it to the project's dependencies)
2. Navigate to Settings > Pylint. On 'Path to Pylint executable' enter the path to pylint.exe which can be found at your ./venv/Scripts/pylint.exe
missing python interpreter config and docker config

###### PostGres
1. Enter the 'pgAdmin 4' app and setup a new dummy database for testing purposes. 
___

### Python Configurations

###### Virtual Environments

Create at Python virtual environment at the root of the project, from where you will work on this project.

```bash
py -m venv .venv
```
To check if you are working in the virtual environment, look at the terminal prompt. If there is a '(.venv)' prefix before the command prompt you are good to go. If it's not the case, run the following command:

[Windows]
```bash
.venv\Scripts\activate
```
[macOS/Linux]
```bash
source .venv/bin/activate
```

###### Python Dependencies
1. Install the uv tool in the virtual environment by running the following command:
```bash
pip install uv
```
2. Install the necessary dependencies for the project in the virtual environment by running the following command:
```bash
uv sync
```
3. If you need to add a dependency to the project, run the following command
```bash
uv add {package} --group {group}
```
___
## 3. Run, Debug and Test

###### Run a FastAPI app
To run the project locally, open a terminal at the root of the project, check if you are using the .venv, and run the following command:
```bash
uvicorn src.{app_folder}.main:app
```
###### Debug
The --reload flag will make the server reload whenever the code is modified, it serves only for development and debugging purposes.
```bash
uvicorn src.{app_folder}.main:app --reload
```
To print debug statements in runtime you must call the uvicorn logger.
```python
import logging

logger = logging.getLogger('uvicorn.error')
logger.debug('This is a debug message')

```
###### Test
To run all tests, run the following command:
```bash
pytest
```
To run a specific set of tests, run the following command:
```bash
pytest {target file or folder}
```
___
## 4. Code formatting and analysis

To format files using Black run the following command:
```bash
black {target file or folder}
```
To format import statements using Isort run the following command:
```bash
isort --profile black {target file or folder}
```
In case you didn't install the Pylint plugin or just want a concise way of viewing Pylint warnings, run the following command:
```bash
pylint {target file or folder}
```
___
## 5. Project Guidelines

Please read all the [Guidelines]()
###### Project Structure

We use a modular approach to structure the project files, as our single repository hosts multiple FastAPI apps that share a significant amount of code. The source folder is organized into subfolders for each app and one for shared code.

Within each app folder, we include app-specific utilities and definitions. Each app’s components are further separated into their own folders, reinforcing the modular structure. In the example below, in the first app, there are separate folders for a GAM client, a PIO client, an auth client, and a router. Each component can also include its own utilities and definitions if needed


    Root/
    ├── src/                   #SourceFiles
    │   ├── app/
    │   │   ├── router/       
    │   │   │   ├── router.py  
    │   │   │   ├── schemas.py #module-specific schemas
    │   │   │   └── models.py  #module-specific models
    │   │   ├── utils/         #app-specific utils
    │   │   └── main.py
    │   └── shared_utils/      #utils shared between all apps
    │       ├── database.py    #database connection
    │       ├── create_app.py
    │       ├── models.py      #global models
    │       └── schemas.py     #global schemas
    ├── tests/                 
    │   ├── app/        #app tests
    │   │   ├── unit_tests/
    │   │   ├── bdd_tests/
    │   │   └── integration_tests/
    ├── Makefile               #Makefile for three musketeers
    ├── pyproject.toml         #Poetry dependencies  
    └── README.md
___