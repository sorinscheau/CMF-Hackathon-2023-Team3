from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, generate_blob_sas, AccountSasPermissions
import uuid
from datetime import datetime, timedelta
import re
import json
from KeyVaultIntegration import get_kv_secret


conn_string = get_kv_secret('sa-conn-string')
split_list = conn_string.split(';')
for item in split_list:
    key, value = item.split('=', maxsplit=1)
    if key == 'AccountName':
        account_name = value
    elif key == 'AccountKey':
        acc_key = value


def get_blob_service_client():
    client_service = BlobServiceClient.from_connection_string(
        conn_string
    )
    return client_service


def get_container_service_client(container_name):
    # # Create the BlobServiceClient object
    client_container = ContainerClient.from_connection_string(
        conn_string,
        container_name=container_name
    )
    return client_container


def get_blob_client(container_name, blob_name):
    # # Create the BlobServiceClient object
    client_blob = BlobClient.from_connection_string(
        conn_string,
        container_name=container_name,
        blob_name=blob_name,
    )
    return client_blob


def create_container(container_name):
    already_created = True
    service_client = get_blob_service_client()
    try:
        service_client.create_container(name=container_name)
        already_created = False
    except Exception as e:
        print(f'Container {container_name} already exists')
    return already_created


def upload_blob(container_name, file):
    blob_client = get_blob_client(container_name, f"{str(uuid.uuid4())}")
    blob_client.upload_blob(file)


def download_blob(container_name, filename):
    blob_client = get_blob_client(container_name, filename)
    downloaded_blob = blob_client.download_blob()
    return downloaded_blob.readall()


def delete_blob(container_name, filename):
    blob_client = get_blob_client(container_name, filename)
    blob_client.delete_blob(delete_snapshots="include")


def list_blobs_flat(container_name):
    container_client = get_container_service_client(container_name)
    blob_list = container_client.list_blobs()
    return blob_list


def get_sas_url(container_name, blob_name):
    url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
    # blob_client = get_blob_client(container_name, blob_name)
    # blob_service_client = get_blob_service_client()
    sas_token = generate_blob_sas(
        account_name=account_name,
        account_key=acc_key,
        container_name=container_name,
        blob_name=blob_name,
        permission=AccountSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)
    )
    url_with_sas = f"{url}?{sas_token}"
    print(url_with_sas)
    return url_with_sas


def save_chat_history(name, history):
    history = json.dumps(history)
    container = name.lower()
    match = re.compile(r'[a-z0-9.]*$')
    if match.match(container):
        if create_container(container):
            file_name_list = list_blobs_flat(container)
            for file in file_name_list:
                delete_blob(container, file.name)
        upload_blob(container, history)


def get_chat_history(name):
    history = None
    container = name.lower()
    match = re.compile(r'[a-z0-9.]*$')
    if match.match(container):
        if create_container(container):  # Container already exists
            file_name_list = list_blobs_flat(container)
            for file in file_name_list:
                response = download_blob(container, file.name)
                response = json.loads(response)
                history = response
    return history
