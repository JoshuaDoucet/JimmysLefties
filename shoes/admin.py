from django.contrib import admin
from shoes.models import Shoe, SiteUser, SearchRequest

# Register your models here.
admin.site.register(Shoe)
admin.site.register(SiteUser)
admin.site.register(SearchRequest)