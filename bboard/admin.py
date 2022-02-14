from django.contrib import admin

from .models import Post, Comment, Category, User


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at')
