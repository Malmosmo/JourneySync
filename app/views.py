import json
import os
import string
import uuid
from pathlib import Path

from django.shortcuts import render, redirect

from JourneySync.settings import BASE_DIR
from app.forms import UploadForm
from app.models import Room

# ---
validPathChars = string.ascii_letters + string.digits + '-,_~./ '


def consistsOf(s1, s2):
    return all(c in s2 for c in s1)


def upload_handler(request, data_path):
    data_path.mkdir(parents=True, exist_ok=False)

    files = request.FILES.getlist('file_field')
    filepaths = json.loads(request.POST.get('directories'))

    for idx, temp_file in enumerate(files):
        path = filepaths[str(idx)]
        path = "/".join(path.split('/')[1:])

        if consistsOf(path, validPathChars):
            filepath = data_path / path
            dirpath = os.path.dirname(filepath)

            if not os.path.exists(dirpath):
                Path(dirpath).mkdir(parents=True, exist_ok=False)

            with open(filepath, 'wb') as file:
                file.write(temp_file.read())
        else:
            print("could not save", path)


# ---


def home(request):
    code = request.GET.get('code', None)
    if code:
        pk = uuid.UUID(bytes=bytes.fromhex(code))
        room_obj = Room.objects.filter(pk=pk).first()

        if not room_obj:
            return redirect('home')

        return redirect('room', pk=pk)

    return render(request, 'app/home.html')


def room_create(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            room_obj = Room.objects.create()
            data_path = BASE_DIR / f'data/{room_obj.pk}/master'
            upload_handler(request, data_path)

            return redirect('room', pk=room_obj.pk)

        print(form.errors)

    return redirect('home')


def room(request, pk):
    room_obj = Room.objects.filter(pk=pk).first()
    upload = True

    if not room_obj:
        return redirect('home')

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file_field')

        if form.is_valid():
            data_path = BASE_DIR / f'data/{room_obj.pk}/new'
            upload_handler(request, data_path)
            upload = False

    return render(request, 'app/room.html', context={'code': room_obj.pk.hex, 'upload': upload, 'room': room_obj})
