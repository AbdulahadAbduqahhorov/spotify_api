from django.contrib import admin

from music.models import Artist,Album,Song

admin.site.register([Artist,Album,Song])


