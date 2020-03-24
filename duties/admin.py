from django.contrib import admin

from duties import models

admin.site.register(models.Group)
# admin.site.register(models.DutyPerson)
admin.site.register(models.DutyDate)


@admin.register(models.DutyPerson)
class DutyPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'group')
    list_filter = ('group', )
    search_fields = ('first_name', 'last_name')
