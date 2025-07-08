from django.contrib import admin

from pets.models import Pets


class PetsAdmin(admin.ModelAdmin):
    list_display = ['name','date_of_birth','pet_img']


admin.site.register(Pets, PetsAdmin)