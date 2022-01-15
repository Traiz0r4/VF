from django.db import models


class SearchBox(models.Model):
    search = models.CharField('Название', max_length=50)


