from ninja import Schema
from datetime import datetime


class Search(Schema):
    id: int
    search_text: str
    min_price: int
    max_price: int


class Product(Schema):
    id: int
    search_id: int

    type: str
    name: str

    price: int
    weight: int

    country: str
    company: str = None

    rating: float
    count_feedback: int

    is_in_stock: bool

    link: str

    search_id: int

    #TODO: image = models.ImageField("Image", upload_to='main_page', blank=True)