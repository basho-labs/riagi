import uuid
from riak import RiakClient, RiakHttpTransport
from django.conf import settings

class UsersRiakService:
    def __init__(self):
        self.users_bucket = settings.RIAK_USERS_BUCKET
        self.riak = RiakClient(host=settings.RIAK_HOST, port=settings.RIAK_PORT)

    def save(self, user_data):
        key = self.generate_key()
        user = self.riak.bucket(self.users_bucket).new(key, user_data)
        user.store()
        return key

    def get(self, user_id):
        user = self.riak.bucket(settings.RIAK_USERS_BUCKET).get(str(user_id))
        if user.exists():
            return user.get_data()
        else:
            return None

    def generate_key(self):
        return uuid.uuid1().hex
