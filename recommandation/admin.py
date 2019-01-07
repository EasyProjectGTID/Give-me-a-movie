from django.contrib import admin

from django.contrib import admin
from .models import Series, KeyWords, Posting, Rating


@admin.register(Series)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(KeyWords)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Posting)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass