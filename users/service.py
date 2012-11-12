import uuid
from riak import RiakClient, RiakHttpTransport
from django.conf import settings

import hashlib
from django.utils.encoding import smart_str
from django.utils.crypto import constant_time_compare

UNUSABLE_PASSWORD = '!'  # This will never be a valid hash
ALLOWEDCHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError(
                '"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def get_random_string(length=12, allowed_chars=ALLOWEDCHARS):
    """
    Returns a random string of length characters from the set of a-z, A-Z, 0-9
    for use as a salt.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit salt. log_2((26+26+10)^12) =~ 71 bits
    """
    import random
    try:
        random = random.SystemRandom()
    except NotImplementedError:
        pass
    return ''.join([random.choice(allowed_chars) for i in range(length)])


def check_password(raw_password, enc_password):
    """
    Returns a boolean of whether the raw_password was correct. Handles
    encryption formats behind the scenes.
    """
    parts = enc_password.split('$')
    if len(parts) != 3:
        return False
    algo, salt, hsh = parts
    return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))


def is_password_usable(encoded_password):
    return (encoded_password is not None
            and encoded_password != UNUSABLE_PASSWORD)


def make_password(algo, raw_password):
    """
    Produce a new password string in this format: algorithm$salt$hash
    """
    if raw_password is None:
        return UNUSABLE_PASSWORD
    salt = get_random_string()
    hsh = get_hexdigest(algo, salt, raw_password)
    return '%s$%s$%s' % (algo, salt, hsh)


class UserService:
    def __init__(self):
        self.users_bucket = settings.RIAK_USERS_BUCKET
        self.riak = RiakClient(host=settings.RIAK_HOST,
                               port=settings.RIAK_PORT)

    def save(self, user_data):
        key = self.generate_key()
        password = user_data['password']
        user_data['encrypted_password'] = make_password('sha1', password)
        del user_data['password']
        user = self.riak.bucket(self.users_bucket).new(key, user_data)
        user.store()
        return key

    def get(self, user_id):
        user = self.riak.bucket(settings.RIAK_USERS_BUCKET).get(str(user_id))
        if user.exists():
            return user.get_data()
        else:
            return None

    def login(self, username, password):
        try:
            user = self.riak.search(settings.RIAK_USERS_BUCKET,
                                    "username:%s" % username).run()
        except ValueError:
            user = None

        if user:
            user = user[0]
            user.set_bucket(str(user.get_bucket()))
            user.set_key(str(user.get_key()))
            user_data = user.get().get_data()
            if check_password(password, user_data['encrypted_password']):
                return user
            else:
                return False
        else:
            return False

    def generate_key(self):
        return uuid.uuid1().hex
