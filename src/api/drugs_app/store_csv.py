from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import ValidationError


class CSVFiles:
    def __init__(self, request) -> None:
        self.request = request
        self.fs = FileSystemStorage()
        pass

    def store_csv_file(self):
        if not self.request.FILES.get("file", ""):
            raise ValidationError("there is not file uploaded")
        file = self.request.FILES.get("file").read()
        content = ContentFile(file)
        temp_file = self.fs.save(name="data.csv", content=content)
        return temp_file

    def get_csv_file(self):
        file = self.fs.path(self.store_csv_file())
        return file
