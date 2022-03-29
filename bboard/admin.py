from django.contrib import admin

from .models import Bb
from .models import Rubric, CarBrands, CarModels


class BbAdmin(admin.ModelAdmin):  # измнение вывода инф-ии
    list_display = ('title', 'content', 'price', 'published', 'rubric')  # что отображается
    list_display_links = ('title', 'content')  # что является ссылкой
    search_fields = ('title', 'content')  # добавление поиска по указанным полям


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(CarBrands)
admin.site.register(CarModels)
