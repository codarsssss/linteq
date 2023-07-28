import os
import shutil
from datetime import datetime
from .models import FileData


def clear_func():
    objects_for_del = FileData.objects.filter(delete_date__lt=datetime.now())
    for i in objects_for_del:
        if os.path.exists(i.path):
            shutil.rmtree(i.path, ignore_errors=False)

    objects_for_del.delete()
