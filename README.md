# Welcome to recipes

## Pre requisites

Run `tk login`, `make init` and `source .venv/bin/activate`


## How to run locally

To locally run the project you only need to do:

```bash
make setup-lambda-runtime-init  # temporarily necessary in macOS to avoid performance problems, see https://github.com/localstack/lambda-runtime-init/pull/28
docker-compose up
```

This will replicate the infrastructure locally and leave you a message with the URLs that point
to your lambda functions. It has hot-reload so you can modify the code and see the changes instantly.

Before spinning up your local infrastructure it will install the dependencies (if it detects a change)
so, for any change in the requirements to take effect, you need to stop docker-compose and start it again.

### Local issues troubleshooting

If something is not going well for docker-compose up regarding pulumi version or pulumi stacks, you can perform a
clean startup by removing your local `volume` and `pulumi_docker` folders in your repository folder to force pulumi
reinstall and localstack volume setup.

For a completely docker cleanup, you can additionally remove all the related docker containers in a stoped state:
```
docker ps -a
```
And remove the stoped containers with the service name
```
docker rm conainerId_1  containerId_2 . . .
```

## How to run tests

```bash
make test
```

## How to debug your code locally

Debugging your code in a lambda function is not as straightforward as in a regular Python project. To perform this task, you need to follow the steps below:
1. The default remote debug port is set to `12345`. This can be changed in the `pulumi-local.yaml` file, `DEBUGGING_PORT` variable. `DEBUG` variable should be set to `true` to enable the remote debugging.
2. Create a new run configuration in PyCharm using the `Python Debug Server` template:
     - Use the same port as the one defined in the `configuration/settings.py` file.
     - Set the host to `localhost`
     - Path mappings: `/YOUR_PROJECT_LOCATION/recipes/src=/var/task/src`
     - Launch the configuration.
3. Place the breakpoint in the desired line of the code that is immediately after the setup debug line.
4. Happy debugging!

NOTE: If you are having issues with the debugger, make sure that the `pydevd-pycharm` package is installed with the same version as the PyCharm IDE. You can check the version of the package in the PyCharm IDE by going to `Help -> About` and looking for the `PyCharm` version and update the lib version in the `install-lambda-dependencies.sh` file if needed.

## How the project is structured

The project is structured following the guidelines in [this](https://www.notion.so/travelperk/Micro-service-code-structure-e418414bbb8b4482ae83561ed63361c4) doc.
Basically the code is structured in two layers:
    1. api: where the communication with outside world happens. Here there should not be any business logic.
    2. application: where the business logic lives.

## How to commit

This project has pre-commit hooks that assure that the code is compliant with TK standards.
In order to run pre-commit hooks you will need to have initialized the repo, see Pre-requisites


## How does this project manage dependencies

Locally, this project relies on virtualenvironments. A virtualenvironment is an isolated sandbox where your dependencies live.
There is a make command to initialize the project (see pre-requisites). Once you have the project initialized you can activate
the virtualenvironment by doing:

```bash
source .venv/bin/activate
```
Most of the editors will do this for you as it is fairly common.


### How to add new dependencies

To add a dependency you will need to modify either the requirements.in or the requirements-dev.in
depending on the type of dependency. After that you will need to call:

```bash
make compile-dependencies
```

Keep in mind that this process relies in pip-tools and pip so make sure you have the requiements installed
(`$pip install -r requirements-dev.txt`) which contain these libraries.
Also know that this will just compile the dependencies, not install them. If you want to install them do it as
usual.


## How does this project manage settings

This project manages settings leveraging the library [pydantic-settings](https://github.com/pydantic/pydantic-settings)
inside the file `src/configuration/settings.py`. This library is capable of doing basic things such as loading from
env variables or coarcing to a specific type.
