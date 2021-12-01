from googleapiclient.discovery import build
import pandas as pd

API_SERVICE_NAME = 'discovery'
API_VERSION = 'v1'
service = build(API_SERVICE_NAME, API_VERSION)
api_service = service.apis()

df_list = pd.DataFrame(api_service.list().execute().get('items'))
print(df_list)

df_methods = pd.DataFrame(api_service.getRest(api='sheets', version='v4').execute())


def save_to_file():
    full_path = r'/Modules/Google/Api_Discovery/api_reference.csv'
    df_methods.to_csv(full_path)


save_to_file()

print(df_methods)
