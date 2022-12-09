from django.contrib import admin
from .models import BoardTemplate, Game, Challenge


# Register your models here.

admin.site.register(BoardTemplate)
admin.site.register(Game)
admin.site.register(Challenge)
