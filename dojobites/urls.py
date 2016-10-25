from django.conf.urls import url, include
from django.contrib import admin

from apps.login_reg_app.models import User
from apps.dojobites_app.models import Restaurant, Date, Comment

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)
class RestaurantAdmin(admin.ModelAdmin):
    pass
admin.site.register(Restaurant, RestaurantAdmin)
class DateAdmin(admin.ModelAdmin):
    pass
admin.site.register(Date, DateAdmin)
class CommentManager(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentManager)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("apps.login_reg_app.urls", namespace="users")),
    url(r'^bites/', include('apps.dojobites_app.urls', namespace='bites')),
]
