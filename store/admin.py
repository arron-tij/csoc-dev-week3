from django.contrib import admin
from store.models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(BookCopy)
admin.site.register(PastRating)