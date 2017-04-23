# cachedir
> Simple file system based caching.

`cachedir` is a simple caching package written in pure Python.
It is primarily designed to support machine learning experiment workflows.

## Features
- Pure Python
- No server, no schema, no fuss
- Simple JSON based storage format (never lose your results)
- Multiprocess safe

## Overview
A cache is represented by the `cachedir.Cache` class and corresponds to a single directory and its contents.
Stored in the cache is a list of write-once entries, each an instance of `cachedir.Entry`.

Each `Entry` has
- A set of JSON serializable attributes which can be accessed using dict syntax.
- An associated directory whose contents can be accessed using the `Entry.contents` method.

An entry's attributes are primarily intended for identification of the associated contents.
For example, command line arguments and various configuration settings can be strored in an entry's attributes. 
On the other hand, the contents of an entry are typically larger objects with specific storage requirements. Pickled python object, serialized model parameters, and datasets should be stored as contents rather than directly in the entry's attributes.

## Example
```python
import cachedir

# Initialize cache
cache = cachedir.Cache('/path/to/cache')

# Creating an entry with a context manager
# automatically saves the entry's attributes
# when the context manager's scope ends.
with cache.create_entry() as entry:
    entry['foo'] = 'some string'
    with open(entry.get_file('words.txt'), 'w') as fp:
        fp.write('\n'.join(['some', 'text', 'in', 'a', 'file']))

# Entries can also be saved manually.
entry = cache.create_entry()
entry['field'] = [1, 2, 3, 4]
entry.save()

# Iterating over entries in a cache is easy.
for i, entry in enumerate(cache):
    print('Entry:', i)
    print(entry.attrs)
    print(entry.contents())

# Outputs
# Entry: 0
# {u'_id': u'/path/to/cache/eXGeOuW', u'foo': u'some string', u'_timestamp': 1492907367.568501}
# [u'/path/to/cache/eXGeOuW/words.txt']
# Entry: 1
# {u'field': [1, 2, 3, 4], u'_id': u'/path/to/cache/eDSQfwS', u'_timestamp': 1492907367.570358}
# []
```