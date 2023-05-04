from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import os


enterprise_app_id = os.environ['AppId']
enterprise_app_secret = os.environ['AppSecret']
keyVaultName = os.environ['KeyVaultName']

tenant_id = 'c166b9c4-5053-4eec-9665-aba0782d0804'
KVUri = f"https://{keyVaultName}.vault.azure.net"


def create_credentials(client_id, client_secret, tenant_id):
    # Create credential object
    credential = ClientSecretCredential(
        client_id=client_id,
        client_secret=client_secret,
        tenant_id=tenant_id
    )
    return credential


def get_kv_secret(secret_name):
    credential = create_credentials(enterprise_app_id, enterprise_app_secret, tenant_id)
    client = SecretClient(vault_url=KVUri, credential=credential)

    retrieved_secret = client.get_secret(secret_name)
    return retrieved_secret.value
