import time
import os
import sys
import json

from .container_api import ContainerApi, OutputFile, LogLevel, ContainerApiError, InputFile

container_api = ContainerApi()


def data_service():

    container_api.log(LogLevel.INFO, "Data Service sample code")
    for i in range(500):
        container_api.log(LogLevel.INFO, "Iteration {i}")
        read = container_api.read_from_file(InputFile.INPUT)

        if read is None:
            container_api.log(LogLevel.INFO, "Break")
            break

        container_api.log(LogLevel.INFO, json.dumps(read))
        read['new-column'] = i
        container_api.append_many_to_file(OutputFile.OUTPUT, [read])