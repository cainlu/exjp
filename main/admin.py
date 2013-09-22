#coding=utf-8

from django.contrib import admin
from models import Item
import os

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('id', 'user', 'context', 'time', 'agree', 'disagree', 'image', 'status')
    list_filter = ('status',)
    list_editable = ('context', 'status',)
    search_fields = ['id', 'context']
    
    def save_model(self, request, obj, form, change):
        if obj.status == 2 and obj.image:
            os.remove(os.getcwd() + '\\' + str(obj.image))
            obj.image = ''
        obj.save()

admin.site.register(Item, ItemAdmin)