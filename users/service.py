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
        return user_data["username"]

    def get(self, username):
        query = "username:%s" % username
        user = self.riak.search(settings.RIAK_USERS_BUCKET, query).run()
        if user:
            user = user[0]
            user.set_bucket(str(user.get_bucket()))
            user.set_key(str(user.get_key()))
            return user.get().get_data()

    def generate_key(self):
        return uuid.uuid1().hex
