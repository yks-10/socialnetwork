from django.contrib import admin
from .models import User, Friendship

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'username')
    list_filter = ('is_deleted', 'created_at')
    search_fields = ('email', 'username')

class FriendshipAdmin(admin.ModelAdmin):
    model = Friendship
    list_display = ('from_user', 'to_user', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('from_user', 'to_user', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Friendship, FriendshipAdmin)
