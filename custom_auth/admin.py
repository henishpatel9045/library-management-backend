from django.contrib import admin
from django.contrib.auth import get_user_model, admin as auth_admin

User = get_user_model()
# Register your models here.
@admin.register(User)
class User(auth_admin.UserAdmin):
    search_fields = ("username",)
     
