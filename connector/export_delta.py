import sys
import os
import json

from .container_api import ContainerApi, InputFile, LogLevel, ContainerApiError, OutputFile

container_api = ContainerApi()


def export():
    container_api.log(LogLevel.INFO, "Export delta example")
    
    for inputFile in [InputFile.NEW, InputFile.MODIFIED]:
        export_products(inputFile)

    delete_products()


def export_products(inputFile: InputFile):
    container_api.log(LogLevel.INFO, "Exporting {} products".format(inputFile))
    for batch in container_api.yield_from_file_batch(inputFile):

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

def delete_products():
    container_api.log(LogLevel.INFO, "Exporting deleted products")
    for batch in container_api.yield_from_file_batch(InputFile.DELETED):
        container_api.log(LogLevel.INFO, json.dumps(batch))

        for product in batch:
            id = product["id"]

            # real connector should use delete products endpoint on 3rd party api
            container_api.log(LogLevel.INFO, "Deleting product id {}".format(product["id"]))