from os.path import basename
from django.conf import settings
import os, glob
from os import path
from zipfile import ZipFile
from .call_fcc import calling_fcc_func
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HstaData, UploadedInputsInfo
from .emss_script import get_image_notes
from .serializers import HstaSerializer
from rest_framework.decorators import api_view
import shutil
import datetime


# Create your views here.


@login_required(login_url='hsta/login')
@api_view(['GET', 'POST'])
def index(request):
    context = {}
    if request.method == 'POST' and request.FILES:
        Zip_File = request.FILES["zip_file"]
        DATA_ID = int(request.POST.get("data_id"))
        print(type(DATA_ID))
        Data = request.data
        current_user = request.user
        file_data = HstaData.objects.get(id=DATA_ID)
        if file_data:
            file_data.zip_file = Zip_File
            file_data.save()
            data_id = DATA_ID
            file_name_saved = HstaData.objects.get(id=data_id)
            user_zip_file_name = Data['zip_file']
            uploaded_zip_file_name = file_name_saved.zip_file.name
            try:
                if path.exists(r"" + settings.MEDIA_ROOT + '/zipped_output_file/'):
                    for f in os.listdir(r"" + settings.MEDIA_ROOT + '/zipped_output_file/'):
                        os.remove(os.path.join(r"" + settings.MEDIA_ROOT + '/zipped_output_file/', f))
                print("====================================================================")
                print("Dict passing to hsta.py module--->", request.session['dict_output'])
                print("====================================================================")
                outputPath = calling_fcc_func(data_id, user_zip_file_name, request.session['dict_output'])
                del request.session['dict_output']

                # create a ZipFile object
                time_stamp = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
                dirName = outputPath
                with ZipFile(str(user_zip_file_name).rsplit('.', 1)[0] + '_' + str(data_id) + '_' + time_stamp + '.zip',
                             'w') as zipObj:
                    # Iterate over all the files in directory
                    for folderName, subfolders, filenames in os.walk(dirName):
                        for filename in filenames:
                            # create complete filepath of file in directory
                            filePath = os.path.join(folderName, filename)
                            # Add file to zip
                            zipObj.write(filePath, basename(filePath))

                HstaData.objects.filter(id=data_id).delete()
                dir_path = os.path.join(settings.MEDIA_ROOT, 'ID' + str(data_id))
                shutil.rmtree(dir_path)
                os.remove(r"" + settings.MEDIA_ROOT + '/' + str(uploaded_zip_file_name))

                zipped_file_name = str(user_zip_file_name).rsplit('.', 1)[0] + '_' + str(
                    data_id) + '_' + time_stamp + '.zip'
                zipped_output = r"" + settings.BASE_DIR + '/' + zipped_file_name
                shutil.move(zipped_output, r"" + settings.MEDIA_ROOT + '/zipped_output_file/')
                outputPath = r"" + 'http://127.0.0.1:8000/media/zipped_output_file/' + zipped_file_name
                context['output'] = outputPath
                user_info = UploadedInputsInfo(user_names=current_user, file_names=user_zip_file_name,
                                               output_status='SUCCESS', date=time_stamp)
                user_info.save()
                messages.success(request, "PROCESS STATUS: SUCCESS")
                return render(request, 'index.html', context)
            except Exception as Err:
                time_stamp = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
                #HstaData.objects.filter(id=data_id).delete()
                dir_path = os.path.join(settings.MEDIA_ROOT, 'ID' + str(data_id))
                shutil.rmtree(dir_path)
                os.remove(r"" + settings.MEDIA_ROOT + '/' + str(uploaded_zip_file_name))
                user_info = UploadedInputsInfo(user_names=current_user, file_names=user_zip_file_name,
                                               output_status='FAIL', date=time_stamp)
                user_info.save()
                context = {"STATUS":"DOWNLOAD DATA", "output": "", "ID": data_id,}
                messages.error(request, "PROCESS STATUS: FAILED --> Error:" + str(Err))
                return render(request, 'index.html', context)
        else:
            HstaData.objects.filter(id=DATA_ID).delete()
            messages.error(request, "May there is some issue with input file!")
            return render(request, 'index.html', context)
    elif request.method == "POST":
        Data = request.data
        current_user = request.user
        serializer = HstaSerializer(data=Data)
        if serializer.is_valid():
            saved_data = serializer.save()
            data_id = saved_data.id
            try:
                request.session['dict_output'], download_link = get_image_notes(Data["title"], Data["chapter"])
                print("----------------------------------------------------------------------")
                print("Dict coming from elseviar site--> ", request.session['dict_output'])
                print("----------------------------------------------------------------------")
                context={
                "STATUS":"DOWNLOAD DATA",
                "output": download_link,
                "ID": data_id,
                }
                messages.success(request, "PROCESS STATUS: SUCCESS")
                return render(request, 'index.html', context)
            except Exception as Err:
                context={
                "STATUS":"ERROR",
                "output": "",
                "ID": data_id,
                }
                messages.error(request, "May be you have entered the 'title' and 'chapter' incorrect!")
                return render(request, 'index.html', context)
        else:
            messages.error(request, "Serializer is not valid!")
            return render(request, 'index.html', context)
    else:     
        return render(request, 'index.html', context)


def log_in(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        context = {}
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                # return render(request, 'index.html')
                return redirect(index)
            else:
                messages.error(request, 'please enter correct credentials!')
                return render(request, 'login.html', context)
        else:
            return render(request, 'login.html')


@login_required(login_url='hsta/login')
def log_out(request):
    auth.logout(request)
    return render(request, 'login.html')
