import time

from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase, CreateError

import riak


class SessionStore(SessionBase):

    def __init__(self, session_key=None):
        RIAK_PORT = getattr(settings, 'RIAK_PORT', 8087)
        RIAK_HOST = getattr(settings, 'RIAK_HOST', "127.0.0.1")
        RIAK_TRANSPORT_CLASS = getattr(settings, 'RIAK_TRANSPORT_CLASS',
                                       riak.RiakPbcTransport)
        RIAK_BUCKET = getattr(settings, 'RIAK_BUCKET', 'django-riak-sessions')
        self._client = riak.RiakClient(host=RIAK_HOST, port=RIAK_PORT,
                                       transport_class=RIAK_TRANSPORT_CLASS)
        self._bucket = self._client.bucket(RIAK_BUCKET)
        super(SessionStore, self).__init__(session_key)

    def load(self):
        # Get the session from Riak.
        session = self._bucket.get(self.session_key)
        if session.exists():
            session_data = session.get_data()
            return self.decode(session_data['data'])
        else:
            self.create()
            return {}

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                # The key wasn't unique, try again
                continue
            self.modified = True
            return

    def save(self, must_create=True):
        session_key = self.session_key
        session_data = self.encode(self._get_session(no_load=must_create))
        expire_date = time.mktime(self.get_expiry_date().timetuple())
        session = self._bucket.new(session_key, data={
            'data': session_data,
            'expire': expire_date,
        })
        # Save the object to Riak.
        session.store()

    def exists(self, session_key):
        session = self._bucket.get(session_key)
        return session.exists()

    def delete(self, session_key=None):
        sk = session_key
        # Get the object and delete it if found.
        if session_key is None:
            sk = self.session_key
        session = self._bucket.get(sk)
        if session.exists():
            session.delete()
