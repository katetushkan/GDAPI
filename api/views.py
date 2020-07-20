import io
from datetime import datetime

from django import views
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload, MediaIoBaseUpload

from api.constants import HOME_DIR, DOWNLOAD_DIR
from api.utils import retrieve_all_files, connect_to_drive, find_files


class MainView(views.View):

    def get(self, request):
        files = retrieve_all_files(connect_to_drive())
        context = {'data': files}

        return render(
            request,
            'index.html',
            context=context
        )

    def post(self, request):
        file_metadata = {'name': request.FILES['myFile'].name}
        f = find_files(file_metadata['name'], HOME_DIR)

        media = MediaFileUpload(f[0], mimetype=request.FILES['myFile'].content_type)

        connect_to_drive().files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        files = retrieve_all_files(connect_to_drive())
        context = {'data': files}

        return render(
            request,
            'index.html',
            context=context
        )


class UploadView(views.View):

    def post(self, request):
        file_name = request.POST['item']
        scope = retrieve_all_files(connect_to_drive())

        for files in scope:
            if files.get('name') == file_name:
                file_id = files.get('id')
                drive_request = connect_to_drive().files().get_media(fileId=file_id)

                full_file_name = DOWNLOAD_DIR + file_name
                fh = io.FileIO(full_file_name, "wb")
                downloader = MediaIoBaseDownload(fh, drive_request)

                done = False
                while not done:
                    status, done = downloader.next_chunk()

        context = {'data': scope}

        return render(
            request,
            'index.html',
            context=context
        )


class VideoView(views.View):

    def post(self, request):
        file_metadata = {'name': datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + '.webm'}
        video = request.FILES['video']
        temp = video.file

        media = MediaIoBaseUpload(temp, mimetype='video/webm')
        connect_to_drive().files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        scope = retrieve_all_files(connect_to_drive())
        context = {'data': scope}

        return render(
            request,
            'index.html',
            context=context
        )
