# -*- coding: utf-8 -*-
from django.db import models


class ExifModelBase(models.Model):
	class Meta:
		abstract = True


class AbstractExifModel(ExifModelBase):
	EXIF_FILE_FIELD = None
	EXIF_DATA_FIELD = None

	class Meta:
		abstract = True
