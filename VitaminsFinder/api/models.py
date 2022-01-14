from django.db import models


# TODO:Add users


class Search(models.Model):
    search_text = models.CharField('Название товара', max_length=255)
    min_price = models.IntegerField('Минимальная цена')
    max_price = models.IntegerField('Максимальная цена')
    update_time = models.TimeField("Время обновления")

    class Meta:
        verbose_name = "Запрос"
        verbose_name_plural = "Запросы"

    def __str__(self):
        return f"{self.search_text} on {self.update_time}"


class Product(models.Model):
    country = models.CharField('Страна', max_length=30)
    type = models.CharField('Тип', max_length=30)
    name = models.CharField('Название',
                            max_length=255,
                            )

    company = models.CharField('Фирма',
                               max_length=255,
                               )

    rating = models.FloatField('Рейтинг')
    count_feedback = models.IntegerField('Количество отзывов')

    price = models.IntegerField('Цена')
    weight = models.IntegerField('Вес')

    is_in_stock = models.BooleanField('В наличии')

    link = models.CharField('Ссылка', max_length=255)

    search = models.ForeignKey('Search', on_delete=models.CASCADE, null=True)

    image = models.ImageField("Image", upload_to='main_page', blank=True)

    def __str__(self):
        return ', '.join(map(str, [
            self.name,
            self.company,
            self.country,
            f'{self.price}р.',
            f'{self.weight}г.',
        ]))

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"