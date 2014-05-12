# -*- coding: utf-8 -*-
from django.db import models
from exif_model.models import AbstractExifModel


class PhotoAlbum(AbstractExifModel):
	EXIF_FILE_FIELD = 'photo_file'
	EXIF_DATA_FIELD = 'exif_data'

	photo_file = models.FileField()
	exif_data = models.TextField()
