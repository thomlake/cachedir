from __future__ import print_function
import shutil

import cachedir


CACHE_LOC = os.path.join(tempfile.gettempdir(), 'cachdir_demo_cache')
# Initialize cache

cache = cachedir.cache(CACHE_LOC)

# Add items
item1 = cache.add({'name': 'foo', 'value': 1})
item2 = cache.add({'name': 'foo', 'value': [2, 3, 4]})
item3 = cache.add({'name': 'bar', 'value': 1})

# Create a file associated with item1
with open(item1.get_path('words.txt'), 'w') as fp:
    fp.write('\n'.join(['some', 'text', 'in', 'a', 'file']))

# Iterate over items in the cache.
print('Items')
for i, item in enumerate(cache.items()):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())

# Iterate over items in the cache with name == "foo".
print('\nItems with name == "foo"')
for i, item in enumerate(cache.items({'name': 'foo'})):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())

# Iterate over items in the cache with value == 1.
print('\nItems with name == "foo"')
for i, item in enumerate(cache.items({'value': 1})):
    print(i, '=>', item)
    print('  name:', item['name'])
    print('  value:', item['value'])
    print('  contents:', item.contents())

shutil.rmtree(CACHE_LOC)