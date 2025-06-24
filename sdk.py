from cognite.client import CogniteClient, ClientConfig, config, global_config
from cognite.client.credentials import OAuthClientCredentials # 'az-dxb-001'

global_config.disable_ssl = True

CDF_TENANT = ''
CDF_PROJECT = 'xyz-project-name'
CDF_BASE_URL = f'https://p001.plink.{CDF_TENANT}.cognitedata.com'
SCOPES = [f'https://{CDF_TENANT}.cognitedata.com/.default']

AZURE_TENANT_ID = ""
AZURE_CLIENT_ID = ""
AZURE_CLIENT_SECRET = ""

def get_client():
    cnf = ClientConfig(client_name="YOUR_APP_NAME",
                       base_url=CDF_BASE_URL,
                       project=CDF_PROJECT,
                       credentials=OAuthClientCredentials(
                           token_url=f'https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/v2.0/token',
                           client_id=AZURE_CLIENT_ID,
                           client_secret=AZURE_CLIENT_SECRET,
                           scopes=SCOPES,
                       ))

    client = CogniteClient(cnf)

    return client