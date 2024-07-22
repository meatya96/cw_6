from django.contrib import admin

from main.models import Client, Message, NewsLetter, SendAttemp


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message')
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    search_fields = ('title',)


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('message', 'status')


@admin.register(SendAttemp)
class SendAttempLogsAdmin(admin.ModelAdmin):
    list_display = ('newsletter',)