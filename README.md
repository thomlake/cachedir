# cachedir
> simple file system based caching

`cachedir` is a simple caching package written in pure Python.
It is primarily designed to support ad-hoc experiment workflows.

- [Features](#features)
- [Overview](#overview)
- [Example](#example)
- [Philosophy](#philosophy)

<a name="features"></a>
## Features
- Pure Python
- No server, no schema, no fuss
- Simple JSON based storage format (never lose your results)
- Multiprocess safe

<a name="overview"></a>
## Overview
A cache is represented by the `cachedir.cache` class and corresponds to a single directory and its contents. Stored in the cache is a list of write-once items, each an instance of `cachedir.item`.

Each `item` has
- A set of JSON serializable attributes which can be accessed using dict syntax.
- A directory whose contents are associated with the item. 

An item's attributes are primarily intended for identification of the associated contents (like a key). For example, command line arguments and various configuration settings can be strored in an item's attributes. The `cachedir.cache` class provides functionality for structural and functional item matching (see the example below for details).

On the other hand, an item's contents are typically larger objects with specific storage requirements. Pickled python objects, serialized model parameters, and datasets should be stored as contents rather than attributes.

An item's attributes always contain two special keys; `@`, which stores the path to the directory associated with the item, and `$`, which stores the time the item was added to the cache. Items also provide a `get_path` method, which can be used to retrieve the absolute path to a (possible non-existant) object in the file system associated with the item, and a `contents` method, which returns a list of files associated with the item.

<a name="example"></a>
## Example
```python
import cachedir

# Initialize cache
cache = cachedir.cache('/tmp/cache')

# Add items
item1 = cache.add({'name': 'foo', 'value': 1})
item2 = cache.add({'name': 'foo', 'value': [2, 3, 4]})
item3 = cache.add({'name': 'bar', 'value': 1})

# Create a file associated with item1
with open(item1.get_path('words.txt'), 'w') as fp:
    fp.write('\n'.join(['some', 'text', 'in', 'a', 'file']))

# Iterate over items in the cache.
for i, item in enumerate(cache.find()):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())
# Output
# 0 => cachedir.item(@=/tmp/cache/item_u2Qoh7, $=2017-04-23 10:45:49)
#   name: foo
#   value: 1
#   contents: [u'/tmp/cache/item_u2Qoh7/words.txt']
# 1 => cachedir.item(@=/tmp/cache/item_fimKg9, $=2017-04-23 10:45:49)
#   name: foo
#   value: [2, 3, 4]
#   contents: []
# 2 => cachedir.item(@=/tmp/cache/item_PX8NrH, $=2017-04-23 10:45:49)
#   name: bar
#   value: 1
#   contents: []

# Iterate over items in the cache with name == "foo".
for i, item in enumerate(cache.find({'name': 'foo'})):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())
# Output
# 0 => cachedir.item(@=/tmp/cache/item_u2Qoh7, $=2017-04-23 10:45:49)
#   name: foo
#   value: 1
#   contents: [u'/tmp/cache/item_u2Qoh7/words.txt']
# 1 => cachedir.item(@=/tmp/cache/item_fimKg9, $=2017-04-23 10:45:49)
#   name: foo
#   value: [2, 3, 4]
#   contents: []

# Iterate over items in the cache with value == 1.
for i, item in enumerate(cache.find({'value': 1})):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())
# Output
# 0 => cachedir.item(@=/tmp/cache/item_u2Qoh7, $=2017-04-23 10:45:49)
#   name: foo
#   value: 1
#   contents: [u'/tmp/cache/item_u2Qoh7/words.txt']
# 1 => cachedir.item(@=/tmp/cache/item_PX8NrH, $=2017-04-23 10:45:49)
#   name: bar
#   value: 1
#   contents: []
```

<a name="philosophy"></a>
## Philosophy
### Why?
`cachedir` is primarily designed to a alleviate a particular machine learning anti-pattern I've frequently encountered (and used) for storing experiment results, the *file name with parameters pattern*. If you've ever encountered a directory filled with folders or files that look like
```
model_layer_sizes_1024_2048_2048_lr_0.01_l2_penalty_0.0001_etc_etc
model_layer_sizes_1024_2048_2048_lr_0.001_max_grad_norm_10_etc_etc
...
```
you'll know exactly what I'm talking about. If you're thinking, "you should really use a database for this sort of thing," you're probably a.) correct, and b.) significantly more principled than I am.

### Simple
Above all else, `cachedir` is designed with simplicity in mind. The items in a cache are literally stored as a newline delimited list of JSON objects in a single file and can be retrieved with two lines of Python:

```python
with open('/path/to/cache/_entries') as fp:
    items = [json.loads(line) for line in fp]
```

This means even if `cachedir` was to undergo a massive rewrite, accessing items in an old cache would be relatively painless. 

Additionally, `cachedir` only has a single non-standard library dependency, [filelock](https://github.com/benediktschmitt/py-filelock), so it should be easy to use anywhere your code might need to run.

### Flexible
Because `cachedir` facilitates easily linking filesystem objects to an item, you are free to choose whatever storage format best suits a particular piece of data (HDF5, JSON, npz, pickle, etc).
