import sha
import base64
import uuid
from datetime import datetime

from riak import RiakClient
from django.conf import settings

class ImageService:
    def __init__(self):
        self.riak = RiakClient(host=settings.RIAK_HOST, port=settings.RIAK_PORT)
        self._metadata_bucket = self.riak.bucket(settings.RIAK_METADATA_BUCKET)
        self._image_bucket = self.riak.bucket(settings.RIAK_IMAGE_BUCKET)

    def store(self, file, user, content_type):
        key = self.create_unique_key()
        filename = self.filename_for_image(key, content_type)
        data = {"user": user,
                "uploaded_at": datetime.utcnow().isoformat(),
                "filename": filename}

        metadata = self._metadata_bucket.new(key, data, content_type="application/json")
        metadata.store()

        image = self._image_bucket.new_binary(key, file, content_type)
        image.store()
        return key

    def find_metadata(self, image_id):
        image = self._metadata_bucket.get(image_id)
        if image.exists():
            return image.get_data()
        else:
            return None

    def find(self, image_id):
        image = self._image_bucket.get_binary(image_id)
        if image.exists():
            return image
        else:
            return None

    def find_all(self, user):
        images = self.riak.search(settings.RIAK_METADATA_BUCKET, "user:%s" % user).map("""function(value) {
         var doc = Riak.mapValuesJson(value)[0];
         doc['id'] = value.key;
         return [doc];
       }""").run()
        return images

    def create_unique_key(self, length=6):
        unique = False
        while not unique:
            id = self.unique_key(length)
            if not self._image_bucket.get(id).exists():
                return id

    def unique_key(self, length=6):
        return base64.b64encode(sha.new(uuid.uuid1().hex[0:7]).hexdigest()[0:7])[0:length]
        
    def filename_for_image(self, key, content_type):
        if content_type in ['image/jpg', 'image/jpeg']:
            extension = 'jpg'
        elif content_type == "image/png":
            extension = 'png'
        elif content_type == 'image/gif':
            extension = 'gif'

        return "%s.%s" % (key, extension)