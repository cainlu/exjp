#coding=utf-8

from django.contrib import admin
from models import Item

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('id', 'user', 'context', 'time', 'agree', 'disagree', 'image', 'status')
    list_filter = ('status',)
    list_editable = ('context', 'status',)
    search_fields = ['id', 'context']

admin.site.register(Item, ItemAdmin)