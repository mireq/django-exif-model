# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models

import json

from .parser import GExiv2Parser
from .settings import EXIF_DATA_PARSER


class ExifModelBase(models.Model):
	class Meta:
		abstract = True


class AbstractExifModel(ExifModelBase):
	EXIF_FILE_FIELD = None
	EXIF_DATA_FIELD = None

	class Meta:
		abstract = True

	def should_save_exif(self):
		return self.EXIF_FILE_FIELD and self.EXIF_DATA_FIELD

	def save_exif(self, file_field, data_field):
		metadata = self.parse_exif(getattr(self, file_field))
		setattr(self, data_field, json.dumps(metadata))

	def get_parser_class(self):
		from django.utils.module_loading import import_string
		return import_string(getattr(settings, 'EXIF_DATA_PARSER', EXIF_DATA_PARSER))

	def parse_exif(self, field):
		parser_class = self.get_parser_class()
		parser = parser_class(filebuf=field.read())
		return parser.metadata

	def save(self, *args, **kwargs):
		if self.should_save_exif() and getattr(self, self.EXIF_FILE_FIELD):
			self.save_exif(self.EXIF_FILE_FIELD, self.EXIF_DATA_FIELD)
		return super(AbstractExifModel, self).save(*args, **kwargs)

