from django.contrib import admin

from .models import UserToken


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    date_hierarchy = "user__date_joined"
    list_display = ["user_username", "key"]
    list_display_links = ["user_username", "key"]
    list_per_page = 10

    @admin.display
    def user_username(self, obj):
        return obj.user.username
