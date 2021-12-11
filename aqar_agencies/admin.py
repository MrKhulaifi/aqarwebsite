from django.contrib import admin

from .models import Agency, AgencyMember, Area, Post, Comment


admin.site.register(Agency)
admin.site.register(AgencyMember)
admin.site.register(Area)
admin.site.register(Post)
admin.site.register(Comment)

# Register your models here.
# superuser: mrkhulaifi, password: open4khulaifi
# user logout url: http://127.0.0.1:8000/accounts/logout
