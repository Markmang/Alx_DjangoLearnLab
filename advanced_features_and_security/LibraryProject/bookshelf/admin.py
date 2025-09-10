from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date',)
    search_fields = ('title', 'author')
    list_filter = ('author', 'published_date')

admin.site.register(Book, BookAdmin)




class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("date_of_birth", "profile_photo")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
