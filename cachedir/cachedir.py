import filelock
import json
import os
import tempfile
import time

from datetime import datetime


WILDCARD = any
def is_wild(x):
    return x == WILDCARD


def matches_structure(a, b):
    """Test if a is a substructure of b.

    matches_structure(
        {'a': 1, 'c': {'x': any}},
        {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}) => True
    matches_structure(
        {'a': 1, 'e': any},
        {'a': 1, 'b': 2, 'c': {'x': 'foo', 'y': 'bar'}, 'd': [1, 2, 3]}) => False
    """
    if is_wild(a):
        return True
    elif isinstance(a, dict):
        if not isinstance(b, dict):
            return False
        for k, v in a.items():
            if k in b and matches_structure(v, b[k]):
                continue
            else:
                return False
        return True
    else:
        return a == b


class item(object):
    """An item in the cache.
    
    Each `item` has
    - A set of JSON serializable attributes which can be accessed using dict syntax.
    - A directory whose contents are associated with the item. 
    """
    def __init__(self, attrs):
        self.attrs = attrs

    def __repr__(self):
        _id = self.attrs['@']
        _timestamp = datetime.fromtimestamp(self.attrs['$'])
        return 'cachedir.item(@={}, $={:%Y-%m-%d %H:%M:%S})'.format(_id, _timestamp)

    def __contains__(self, key):
        return key in self.attrs

    def __getitem__(self, key):
        return self.attrs[key]

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def contents(self):
        """Get the paths to files associated with this item."""
        root = self.attrs['@']
        filepaths = []
        for path, _, filenames in os.walk(root):
            for fn in filenames:
                filepaths.append(os.path.join(path, fn))
        return filepaths

    def get_path(self, *parts):
        """Get the path to a filesystem object associated with this item."""
        return os.path.join(self.attrs['@'], *parts)


def _get_create_lock():
    filename = os.path.join(tempfile.gettempdir(), '__dircache_create_lock__')
    return filelock.FileLock(filename)


class cache(object):
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

    def add(self, attrs=None, prefix='item_'):
        """Add an item to the cache.

        The argument attrs must be JSON serializable.
        
        Two special keys are added to attrs if they do not exist:
        - "@" A new directory for this item's contents.
        - "$" The time this item was added (given by time.time())
        """
        attrs = dict(attrs) if attrs else {}
        attrs['@'] = attrs['@'] if '@' in attrs else tempfile.mkdtemp(prefix=prefix, dir=self.base)
        attrs['$'] = attrs['$'] if '$' in attrs else time.time()
        string = json.dumps(attrs)
        with self.lock:
            with open(self.filename, 'a') as fp:
                fp.write(string)
                fp.write('\n')
                fp.flush()
        return item(attrs)

    def items(self, match=None):
        """Return a list of items in the cache.
        
        If match is None all items are returned.
        If match is callable then all items returned satisfy bool(match(item)) == True.
        Otherwise all items returned satisfy cachedir.matches_structure(match, item) == True.
        """
        if not os.path.exists(self.filename):
            return []
        with self.lock:
            with open(self.filename) as fp:
                items = [item(json.loads(line)) for line in fp]

        if callable(match):
            return [x for x in items if match(x)]
        elif match is not None:
            return [x for x in items if matches_structure(match, x.attrs)]
        return items
