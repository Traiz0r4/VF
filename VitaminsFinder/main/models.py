from django.db import models





class SearchBox(models.Model):
    search_text = models.CharField('Название', max_length=50)
    min_price = models.IntegerField('min price')
    max_price = models.IntegerField('max price')