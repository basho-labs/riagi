# riagi

riagi is a sample application using Riak with Django to implement an
[imgur](http://imgur.com) clone. It uses Riak to store images,
thumbnails, image metadata, user profiles, and sessions.

## Setup

The needed packages are listed in `requirements.txt`, but briefly,
they are:

* Django 1.3
* Python Imaging Library (PIL)
* Riak Python Client (`riak`)
* shortuuid

Once you have those packages installed and Riak available on the local
host in the default configuration,
[enable Riak Search on the Riak node](http://docs.basho.com/riak/latest/references/Riak-Search---Settings/#Enabling-Riak
Search), and then run these two commands to install the search
indexing hooks:

```bash
$ search-cmd install riagi-users
$ search-cmd install riagi-image-metadata
```

Now start up the server:

```bash
$ python manage.py runserver
```

Open your browser to http://localhost:8000/ to view the app. You
should see something like so:

![riagi](https://raw.github.com/basho/riagi/master/screenshot.png)

## License

riagi is licensed under the [Apache v2.0 license](/basho/riagi/blob/master/LICENSE).
