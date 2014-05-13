# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Photo


admin.site.register(Photo, admin.ModelAdmin)
