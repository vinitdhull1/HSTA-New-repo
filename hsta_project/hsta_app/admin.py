from django.contrib import admin
from .models import HstaData, UploadedInputsInfo


# Register your models here.

@admin.register(HstaData)
class HstaAdmin(admin.ModelAdmin):
    list_display = ['id', 'ISBN', 'title', 'author', 'chapter', 'edition', 'zip_file', 'email']


@admin.register(UploadedInputsInfo)
class UploadedInputsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_names', 'file_names', 'output_status', 'date']
