import sys
import os
import json

from datetime import datetime, timedelta, timezone

from .container_api import ContainerApi, InputFile, LogLevel, ContainerApiError, OutputFile

container_api = ContainerApi()

FULL_UPLOAD_INTERVAL = timedelta(days=30)


def export():
    container_api.log(LogLevel.INFO, "Export example")

    # The bucket is shared across all sites of the connector environment,
    # so the state is namespaced by the current site id.
    site = os.environ.get('SITE')
    key = "last-full-upload-{}".format(site)

    now = datetime.now(timezone.utc)
    last_full_upload = read_last_full_upload(key)

    if last_full_upload is not None and now - last_full_upload < FULL_UPLOAD_INTERVAL:
        container_api.log(LogLevel.INFO, "Skipping full send, last sent at {}".format(last_full_upload.isoformat()))
        return

    send_full_feed()

    container_api.write_to_bucket(key, json.dumps({"site": site, "last_full_upload": now.isoformat()}))
    container_api.log(LogLevel.SUCCESS, "Sent full feed, recorded upload at {}".format(now.isoformat()))


def read_last_full_upload(key):
    stored = container_api.read_from_bucket(key)

    # No value yet (first run) or malformed content -> treat as never sent.
    if stored is None:
        return None

    try:
        return datetime.fromisoformat(json.loads(stored)["last_full_upload"])
    except (ValueError, KeyError, TypeError):
        return None


def send_full_feed():
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
