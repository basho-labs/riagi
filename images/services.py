import sha
import base64
import uuid
import httplib
import re
import shortuuid

from urlparse import urlparse
from datetime import datetime
from PIL import Image
from StringIO import StringIO
from tempfile import NamedTemporaryFile
from riak import RiakClient
from django.conf import settings

MAP_DOCID = """function(value) {
                 var doc = Riak.mapValuesJson(value)[0];
                 doc['id'] = value.key;
                 return [doc];
               }"""


class ImageError(Exception):
    pass


class RemoteImage:
    def __init__(self, reader):
        self._temp_file = NamedTemporaryFile()
        print self._temp_file.name
        self._temp_file.write(reader.read())
        self._temp_file.seek(0)

    def temporary_file_path(self):
        return self._temp_file.name

    def read(self):
        return self._temp_file.read()


class ImageService:
    def __init__(self):
        self.riak = RiakClient(host=settings.RIAK_HOST,
                               port=settings.RIAK_PORT)
        self._metadata_bucket = self.riak.bucket(settings.RIAK_METADATA_BUCKET)
        self._image_bucket = self.riak.bucket(settings.RIAK_IMAGE_BUCKET)
        self._thumbs_bucket = self.riak.bucket(settings.RIAK_THUMBS_BUCKET)

    def store_from_url(self, address, user):
        url = urlparse(address)
        if str(url.scheme) != 'http':
            raise ImageError('Not a valid URL')

        if not re.search(r'(jpg|jpeg|png|gif)$', url.path):
            raise ImageError('Unsupported file format')

        http = httplib.HTTPConnection(url.netloc)
        http.request('GET', url.path)
        response = http.getresponse()
        image = RemoteImage(response)
        return self.store(image, user,
                          response.getheader("Content-Type", "image/jpg"))

    def store(self, image, user, content_type):
        key = self.create_unique_key()
        filename = self.filename_for_image(key, content_type)
        data = {"user": user,
                "uploaded_at": datetime.utcnow().isoformat(),
                "filename": filename}

        thumbnail = self.create_thumbnail(image)

        metadata = self._metadata_bucket.new(key, data,
                                             content_type="application/json")
        metadata.store()

        image = self._image_bucket.new_binary(key, image.read(), content_type)
        image.store()

        thumb = self._thumbs_bucket.new_binary(key, thumbnail,
                                               content_type="image/jpeg")
        thumb.store()

        return key

    def create_thumbnail(self, image):
        thumbnail = Image.open(image.temporary_file_path())
        thumbnail.thumbnail((128, 128), Image.ANTIALIAS)
        thumbio = StringIO()
        thumbnail.save(thumbio, format="jpeg")
        return thumbio.getvalue()

    def find_metadata(self, image_id):
        image = self._metadata_bucket.get(image_id)
        if image.exists():
            return image.get_data()
        else:
            return None

    def find(self, image_id, thumb=False):
        if thumb:
            image = self._thumbs_bucket.get_binary(image_id)
        else:
            image = self._image_bucket.get_binary(image_id)
        if image.exists():
            return image
        else:
            return None

    def find_all(self, user):
        images = self.riak.search(settings.RIAK_METADATA_BUCKET,
                                  "user:%s" % user).map(MAP_DOCID).run()
        return images

    def create_unique_key(self, length=6):
        unique = False
        while not unique:
            id = self.unique_key(length)
            if not self._image_bucket.get(id).exists():
                return id

    def unique_key(self, length=6):
        return shortuuid.uuid()[0:length]

    def filename_for_image(self, key, content_type):
        if content_type in ['image/jpg', 'image/jpeg']:
            extension = 'jpg'
        elif content_type == "image/png":
            extension = 'png'
        elif content_type == 'image/gif':
            extension = 'gif'

        return "%s.%s" % (key, extension)
