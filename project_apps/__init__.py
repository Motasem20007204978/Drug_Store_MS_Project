from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import ValidationError

fs = FileSystemStorage(location="media/files/")


class CSVFiles:
    def __init__(self, request) -> None:
        self.request = request
        pass

    def store_csv_file(self):
        file = self.request.FILES.get("file", "")
        if not file:
            raise ValidationError("there is not file uploaded")
        content = ContentFile(file.read())
        temp_file = fs.save(name="data.csv", content=content)
        return temp_file

    def get_csv_file(self):
        file = fs.path(self.store_csv_file())
        return file
