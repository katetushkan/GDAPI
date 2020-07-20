import os

from googleapiclient import discovery, errors
from httplib2 import Http
from oauth2client import file, client, tools

from api.constants import CREDENTIALS_PATH, CLIENT_SECRET_PATH, GOOGLE_SCOPE


def find_files(filename, search_path):
    result = []

    for root, directory, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))

    return result


def connect_to_drive():
    store = file.Storage(CREDENTIALS_PATH)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_PATH, GOOGLE_SCOPE)
        credentials = tools.run_flow(flow, store)

    http = credentials.authorize(Http())
    drive = discovery.build('drive', 'v3', http=http)

    return drive


def retrieve_all_files(api_service):
    list_of_files = []
    page_token = None

    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token

            files = api_service.files().list(**param).execute()
            list_of_files.extend(files.get('files'))

            page_token = files.get('nextPageToken')
            if not page_token:
                break

        except errors.HttpError as e:
            break

    return list_of_files
