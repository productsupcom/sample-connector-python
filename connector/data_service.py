import sys
import os
import json

from .container_api import ContainerApi, OutputFile, LogLevel, ContainerApiError, InputFile

container_api = ContainerApi()


def data_service():
    new_column = os.environ.get('NEW_COLUMN_NAME')
    source_column = os.environ.get('SOURCE_COLUMN')

    if not new_column or not source_column:
        container_api.log(LogLevel.ERROR, "Source or target column empty. Please check data service configuration in the platform")
        sys.exit(1)

    container_api.log(LogLevel.INFO, "Copy data from {} to new column {}".format(source_column, new_column))

    # read all products in batches of 100
    for batch in container_api.yield_from_file_batch(InputFile.FULL):

        container_api.log(LogLevel.INFO, json.dumps(batch))

        # modify / filter / enrich the products
        for product in batch:
            product[new_column] = product[source_column]

        # push products to the current productsup site
        # note: even if products are not modified, you have to push them, otherwise the products will disappear.
        # if no products are pushed it will wipe out all the products
        container_api.append_many_to_file(OutputFile.OUTPUT, batch)