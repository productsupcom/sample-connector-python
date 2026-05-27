import typing

from enum import StrEnum

import httpx

from .cde_container_api_client import Client

from .cde_container_api_client.models import WriteToOutputFileInput, WriteToOutputFileInputMeta, \
    WriteToOutputFileInputDataItem, WriteToOutputFileResponse400
from .cde_container_api_client.api.file import write_to_output_file

from .cde_container_api_client.models import WriteLogInput, WriteLogInputContext, WriteLogResponse400
from .cde_container_api_client.api.log import write_log

from .cde_container_api_client.api.file import read_input_file_next, read_input_file_next_batch
from .cde_container_api_client.models import ReadInputFileNextBatchResponse400


class ContainerApiError(Exception):
    def __init__(self, message: str):
        self.message = message


class OutputFile(StrEnum):
    OUTPUT = 'output'
    FEEDBACK = 'feedback'

class InputFile(StrEnum):
    FULL = 'full'
    NEW = 'new'
    MODIFIED = 'modified'
    UNCHANGED = 'unchanged'
    DELETED = 'deleted'

class LogLevel(StrEnum):
    SUCCESS = 'success'
    DEBUG = 'debug'
    INFO = 'info'
    NOTICE = 'notice'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
    ALERT = 'alert'
    EMERGENCY = 'emergency'
    REPORT = 'report'


class ContainerApi:
    client: Client

    def __init__(self):
        self.client = Client(base_url="http://cde-container-api")

    def append_to_file(self,
                       file: OutputFile,
                       item: dict,
                       separator: typing.Optional[str] = None):
        return self.append_many_to_file(file, [item], separator)

    def append_many_to_file(self,
                            file: OutputFile,
                            items: list,
                            separator: typing.Optional[str] = None):
        body = WriteToOutputFileInput()
        body.data = [WriteToOutputFileInputDataItem.from_dict(item) for item in items]

        if separator is not None:
            meta = WriteToOutputFileInputMeta()
            meta.separator = separator
            body.meta = meta

        response = write_to_output_file.sync(file, client=self.client, json_body=body)
        if type(response) is WriteToOutputFileResponse400:
            raise ContainerApiError('{} {}'.format(response.message, response.errors.to_dict()))

        return response

    def read_from_file(self,
                       file: InputFile):
        response = read_input_file_next.sync(file, client=self.client)

        if response is None:
            return None

        return response.data.to_dict()

    def read_from_file_batch(self,
                             file: InputFile,
                             batch_size: int = 100):
        response = read_input_file_next_batch.sync(file, client=self.client, size=batch_size)

        if response is None or not response.data:
            return None
        
        if type(response) is ReadInputFileNextBatchResponse400:
            raise ContainerApiError('{} {}'.format(response.message, response.errors.to_dict()))

        return [response_item.to_dict() for response_item in response.data]

    def yield_from_file_batch(self, 
                              file: InputFile,
                              batch_size: int = 100):
        while True:
            products = self.read_from_file_batch(file, batch_size)
            
            if products is None:
                break

            yield products

    def log(self,
            level: str,
            message: str,
            context: typing.Optional[dict] = None):
        body = WriteLogInput()
        body.message = message

        if context is not None:
            body.context = WriteLogInputContext.from_dict(context)

        response = write_log.sync(level, client=self.client, json_body=body)
        if type(response) is WriteLogResponse400:
            raise ContainerApiError('{} {}'.format(response.message, response.errors.to_dict()))

        return response

    def write_to_bucket(self, key: str, data: str) -> None:
        response = self._bucket_request('put', key, content=data)
        if not response.is_success:
            raise ContainerApiError('Failed to write bucket key {} (status {})'.format(key, response.status_code))

    def read_from_bucket(self, key: str) -> typing.Optional[str]:
        response = self._bucket_request('get', key)
        if not response.is_success:
            return None

        return response.text

    def _bucket_request(self, method: str, key: str, content: typing.Optional[str] = None) -> httpx.Response:
        url = "{}/buckets/stream/{}".format(self.client.base_url, key)

        return httpx.request(
            method=method,
            url=url,
            headers=self.client.get_headers(),
            cookies=self.client.get_cookies(),
            timeout=self.client.get_timeout(),
            follow_redirects=self.client.follow_redirects,
            verify=self.client.verify_ssl,
            content=content,
        )
