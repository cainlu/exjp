#coding=utf-8

from django.contrib import admin
from models import Item, Item_Ready
import os

class Item_Admin(admin.ModelAdmin):
    model = Item
    list_display = ('id', 'user', 'context', 'time', 'agree', 'disagree', 'image', 'status',)
    list_filter = ('status',)
    list_editable = ('context', 'status',)
    search_fields = ['id', 'context']
    
    def save_model(self, request, obj, form, change):
        if obj.status == 2 and obj.image:
            os.remove(os.getcwd() + '/' + str(obj.image))
            obj.image = ''
        obj.save()

class Item_Ready_Admin(admin.ModelAdmin):
    model = Item_Ready
    list_display = ('id', 'context', 'image', 'status',)
    list_editable = ('context', 'image', 'status',)

admin.site.register(Item, Item_Admin)
admin.site.register(Item_Ready, Item_Ready_Admin)