# -*- coding: utf-8 -*-
from django.utils.functional import cached_property


class BaseParser(object):
	class ParseError(Exception):
		pass

	@cached_property
	def metadata(self):
		return self.get_metadata()

	def get_metadata(self):
		raise NotImplementedError

	def get_metadata_tag(self, tag, default=None):
		return self.metadata.get(tag, default)

	def set_metadata_tag(self, tag, value):
		raise NotImplementedError

	def save_to_file(self):
		raise NotImplementedError


class GExiv2Parser(BaseParser):
	def __init__(self, filename=None, filebuf=None):
		from gi.repository import GExiv2
		from gi.repository import GObject
		self.exif = GExiv2.Metadata()
		self.changed = False
		try:
			if filebuf is None:
				self.exif.open_path(filename)
			else:
				self.exif.open_buf(filebuf)
		except GObject.GError:
			raise GExiv2Parser.ParseError("Bad image format")

	def get_metadata(self):
		return dict((t, self.exif.get_tag_string(t)) for t in self.exif.get_tags())

	def set_metadata_tag(self, tag, value):
		self.exif.set_tag_string(tag, value)
		self.changed = True

	def save_to_file(self):
		if self.changed:
			self.exif.save_file()
