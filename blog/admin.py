from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    list_filter = ('title',)
    search_fields = ('content',)
    readonly_fields = ('views', 'published_date')

