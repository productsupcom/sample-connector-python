import sys
import os
import json

from .container_api import ContainerApi, InputFile, LogLevel, ContainerApiError, OutputFile

container_api = ContainerApi()


def export():
    container_api.log(LogLevel.INFO, "Export example")

    # read all products in batches of 100
    for batch in container_api.yield_from_file_batch(InputFile.FULL):

        container_api.log(LogLevel.INFO, json.dumps(batch))

        for product in batch:
            id = product["id"]

            # real connector should export products to 3rd party api
            container_api.log(LogLevel.INFO, "Exporting product id {}".format(product["id"]))
            
            if id == "1":
                container_api.append_to_file(OutputFile.FEEDBACK, {
                    "id": id,
                    "error": "Can not export product due to api failure"
                })
