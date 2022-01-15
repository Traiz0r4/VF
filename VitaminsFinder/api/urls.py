from django.contrib import admin
from django.urls import path
from typing import List
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from . import models, schemas

api = NinjaAPI()


@api.get("/product/{id}", response=schemas.Product)
def get_product(request, product_id):
    return get_object_or_404(models.Product, id=product_id)


@api.get("/search/{id}", response=schemas.Search)
def get_search(request, search_id):
    return get_object_or_404(models.Search, id=search_id)


@api.post("/search")
def create_search(request, search: schemas.Search):
    cur_search = models.Search.objects.create(**search.dict())
    # TODO: get from IHerb best products

    products = []
    for product in products:
        product["search_id"] = cur_search.pk

    return cur_search


@api.post("/product")
def create_product(request, product: schemas.Product):
    return models.Product.objects.create(**product.dict())


@api.get("/products_of_search/{search_id}", response=List[schemas.Product])
def get_products_of_search(request, search_id):
    return models.Product.objects.filter(search_id=search_id)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api.urls)
]