# -*- coding: utf-8 -*-
from django.utils.functional import cached_property


class BaseParser(object):
	def __init__(self, filename):
		self.filename = filename

	@cached_property
	def metadata(self):
		raise NotImplementedError

	def get_metadata_tag(self, tag, default=None):
		return self.metadata.get(tag, default)

	def set_metadata_tag(self, tag, value):
		raise NotImplementedError

	def save_to_file(self):
		raise NotImplementedError


class GExiv2Parser(BaseParser):
	def __init__(self, filename):
		super(BaseParser, self).__init__(filename)

		from gi.repository import GExiv2
		self.exif = GExiv2.Metadata(filename)
		self.changed = False

	def metadata(self):
		return dict((t, exif.get_tag_string(t)) for t in self.exif.get_tags())

	def set_metadata_tag(self, tag, value):
		self.exif.set_tag_string(tag, value)
		self.changed = True

	def save_to_file(self):
		if self.changed:
			self.exif.save_file()
