# summarizer/models.py
from django.db import models

class Document(models.Model):
    # The uploaded PDF file will be stored in a 'documents/' folder
    file = models.FileField(upload_to='documents/')
    summary = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name