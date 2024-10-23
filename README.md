# Sample Python connector

It provides two types of connectors:
  * Data source - import the data into the Productsup platofrm
  * Data service - manipulate the existing data in Productsup platform

## Create, configure, build, deploy connector in the Developer portal

#### Create connector
* Login into the [Dev portal](https://dev-portal.productsup.com)
* Add new connector with the following attributes:
  * Type: `data source` or `data service`, 
  * Execution mode: `environemnt variable` (Connector will receive configuration options via environment variables)

#### Configure data source connector
* Version control
  * Configure version control based on your VCS provider
* Application
  * Command: `python`
  * Arguments `main.py data-source`
  * Health check: `--health-check`
* Individual configurations
  * Command option: `SHOULD_FAIL`; Field type: `checkbox`
  * Command option: `NAME`; Field type: `input`

#### Configure data service connector
* Version control
  * Configure version control based on your VCS provider
* Application
  * Command: `python`
  * Arguments `main.py data-service`
  * Health check: `--health-check`
* Individual configurations
  * Command option: `NEW_COLUMN_NAME`; Field type: `input`
  * Command option: `SOURCE_COLUMN`; Field type: `stage_columns_dropdown`
* Data service configuration:
  * Service type: `internal`
  * Stage: `import`
  * Column prefix: `___prefix`
  * Max usage: `1`

#### Configure export connector
* Create new channel template for the connector
  * Channels -> Add Channel
  * Add template columns required
* Version control
  * Configure version control based on your VCS provider
* Application
  * Command: `python`
  * Arguments `main.py export`
  * Health check: `--health-check`
* Export configuration
  * Enable feedback file
  * Assign channel for the connector

#### Configure export-delta connector
* Create new channel template for the connector
  * Channels -> Add Channel
  * Add template columns required
  * Mark channel as delta
  * Set delta key on unique id column
* Version control
  * Configure version control based on your VCS provider
* Application
  * Command: `python`
  * Arguments `main.py export-delta`
  * Health check: `--health-check`
* Export configuration
  * Enable feedback file
  * Assign channel for the connector

#### Build, deploy connector
* In the release configuration trigger build. If everything was configured correctly it should succeed.
* Synchronize it with the platform
  * Before you are able to deploy connector to the Productsup platform a CDE admin will need to assign you Platform account to the connector. You can open a request in the developer portal or reach out to your contact person.

## Main features

### Conenctor exit code
Connector exit code determines whether a site run in the platform is marked successful or failed. You should mark run failed when connector can not perform required actions - for example invalid authentication data.
```python
import sys

sys.exit()  # successful run is 0
sys.exit(1) # unsuccessful run is 1
```

### Container API client
Container API is used to interact between connector and the platform. In this demo it is used for:
* Importing products into the platform
* Dispatching log messages, which are visible in the notification section

There is generated client inside `connector/cde_container_api_client`. `connector/container_api.py` wraps it to make it choerent to use.

#### Save products to the platform

```python
from connector.container_api import ContainerApi, OutputFile

container_api = ContainerApi()

products = [
    {'id': 1, 'name': 'first_product'},
    {'id': 2, 'name': 'second product'}
]
container_api.append_many_to_file(OutputFile.OUTPUT, products)
```

#### Publish a log message to the platform
```python
from connector.container_api import ContainerApi, LogLevel

container_api = ContainerApi()

container_api.log(LogLevel.ERROR, 'This is an error message')
container_api.log(LogLevel.INFO, 'This is an info message')
container_api.log(LogLevel.SUCCESS, 'This is a success message')
```

#### Failed container API call
If by any chance an invalid API call is made, `connector/container_api.py` will raise `ContainerApiError` exception.

You can use log endpoint in Container API to log an error.

Alternatively, if for some reason connector can not reach Container API, you can also write an error to `STDERR`. Standard error is behaving the same as `error` log level though Container API. 

```python
import sys
from connector.container_api import ContainerApi, OutputFile, LogLevel, ContainerApiError
container_api = ContainerApi()

products = []
try:
    container_api.append_many_to_file(OutputFile.OUTPUT, products)
except ContainerApiError as error:
    container_api.log(LogLevel.ERROR, error.message)
    # alternatively you can also log to STDERR when there are issues with calling container api
    print(error.message, file=sys.stderr)
```

### Individual configurations
Depending on the connector execution mode (chosen in the step when creating a connector), configurations made by the user in the platform will be passed by:
  * Command line arguments
  * Environemnt variables

In the sample connector environment variables are being used.
The following snippet reads and logs the environment variable
```python
import os

from connector.container_api import ContainerApi, LogLevel
container_api = ContainerApi()

name = os.environ.get('NAME')
if name:
    container_api.log(LogLevel.SUCCESS, 'Hello {}'.format(name))
```
## Notes

#### Client generation
Generated client is included in sample connector. You do not need to regenerate the client unless there are new features available that you need.

To regenerate it, a new container api open API spec file should be fetched from the CDE API and the follow the snippet below.
* Show [Container API versions](https://cde.productsup.com/docs/api/#/ContainerApi/show_container_api_versions)
* Show [Container API Open API spec file](https://cde.productsup.com/docs/api/#/ContainerApi/show_container_api_version_docs) for specific Container API version
```bash 
# update requirements.txt
docker-compose run connector /bin/bash -c "pip install --no-cache-dir -r requirements.txt; pip install openapi-python-client; pip3 freeze > requirements.txt"
# generate client
docker-compose run connector /bin/bash -c "pip3 install openapi-python-client; openapi-python-client generate --path container-api-openapi.json"
# move client to root of the project
mv cde-container-api-client/cde_container_api_client .
```