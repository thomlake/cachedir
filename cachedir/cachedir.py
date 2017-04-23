import filelock
import json
import os
import tempfile
import time

from datetime import datetime

class Entry(object):
    """An entry in the cache.

    - A set of JSON serializable attributes which can be accessed using dict syntax.
    - An associated directory whose contents can be accessed using the `Entry.contents` method.
    """
    def __init__(self, cache, attrs):
        self.cache = cache
        self.attrs = attrs
        self.has_updates = False

    def __repr__(self):
        return 'Entry({}, {:%Y-%m-%d %H:%M:%S})'.format(
            self.attrs['_id'],
            datetime.fromtimestamp(self.attrs['_timestamp']))

    def __setitem__(self, key, value):
        if not isinstance(key, basestring):
            raise ValueError('key must be an instance of basestring (got: {})'.format(type(key)))
        if key == '_id':
            raise ValueError('_id may not be overridden')

        self.has_updates = True
        self.attrs[key] = value

    def __getitem__(self, key):
        return self.attrs[key]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        """Save entry."""
        self.save()

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def update(self, items):
        """Add items to the entries attributes."""
        self.attrs.update(items)

    def save(self):
        """Save this entry in the cache."""
        if not self.has_updates:
            return False
        self.cache.append(self.attrs)
        self.has_updates = False
        return True

    def contents(self, abspath=True):
        """Get the top level contents associated with this entry."""
        folder = self.attrs['_id']
        items = os.listdir(folder)
        if abspath:
            return [os.path.join(folder, item) for item in items]
        return items

    def get_file(self, name):
        """Get the path to a file associated with this entry with the given name."""
        filename = os.path.join(self.attrs['_id'], name)
        return filename


def _get_create_lock():
    filename = os.path.join(tempfile.gettempdir(), '__dircache_create_lock__')
    return filelock.FileLock(filename)


class Cache(object):
    """A file system backed cache."""
    def __init__(self, loc='./cache'):
        base = os.path.abspath(loc)
        if not os.path.exists(base):
            create_lock = _get_create_lock()
            with create_lock:
                if not os.path.exists(base):
                    os.makedirs(base)
        elif not os.path.isdir(base):
            raise ValueError('cache name exists but is not a directory (name: "{}")'.format(base))
            
        self.base = base
        self.lock = filelock.FileLock(os.path.join(self.base, '_lock'))
        self.filename = os.path.join(self.base, '_entries')

    def __iter__(self):
        """Return a list of entries in the cache."""
        if not os.path.exists(self.filename):
            return iter([])
        with self.lock:
            with open(self.filename) as fp:
                return [Entry(self, json.loads(line)) for line in fp]

    def append(self, obj):
        """Append an object to the entries in the cache.

        obj must be JSON serializable.
        """
        string = json.dumps(obj)
        with self.lock:
            with open(self.filename, 'a') as fp:
                fp.write(string)
                fp.write('\n')

    def create_entry(self, attrs=None):
        """Create and return a new entry in the cache."""
        attrs = dict(attrs) if attrs else {}
        _id = tempfile.mkdtemp(prefix='e', dir=self.base)
        _timestamp = time.time()
        attrs.update({'_id': _id, '_timestamp': _timestamp})
        return Entry(self, attrs)
