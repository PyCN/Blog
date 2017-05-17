from django.contrib import admin

# Register your models here.
from blog.models import * 

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BlogComment)
admin.site.register(Permission)
admin.site.register(UserProfile)
admin.site.register(VisitorIP)

