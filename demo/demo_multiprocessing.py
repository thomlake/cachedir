from __future__ import print_function
import multiprocessing
import os
import random
import shutil
import tempfile
import time

import cachedir


CACHE_LOC = os.path.join(tempfile.gettempdir(), 'cachdir_demo_cache')


def work(name):
    cache = cachedir.cache(CACHE_LOC)
    for i in range(5):
        c = cache.add({'name': name, 'iter': i})
        time.sleep(random.random())


if __name__ == '__main__':
    pool = multiprocessing.Pool(2)
    names = ['foo', 'bar', 'qux']
    pool.map(work, names)

    cache = cachedir.cache(CACHE_LOC)
    print('All items')
    for i, entry in enumerate(cache.items()):
        print(i, '=>', entry)

    print('Items with name == "foo"')
    for i, entry in enumerate(cache.items({'name': 'foo'})):
        print(i, '=>', entry)

    print('Items with even "iter"')
    for i, entry in enumerate(cache.items(lambda x: x['iter'] % 2 == 0)):
        print(i, '=>', entry)

    shutil.rmtree(CACHE_LOC)

# Possible output
# ---------------
# 0 => cachedir.item(@=/tmp/cachdir_demo/item_9RKElJ, $=2017-04-23 10:19:02)
# 1 => cachedir.item(@=/tmp/cachdir_demo/item_S1FVBg, $=2017-04-23 10:19:02)
# 2 => cachedir.item(@=/tmp/cachdir_demo/item_1cRfSy, $=2017-04-23 10:19:02)
# 3 => cachedir.item(@=/tmp/cachdir_demo/item_30XOSW, $=2017-04-23 10:19:02)
# 4 => cachedir.item(@=/tmp/cachdir_demo/item_oIPkRy, $=2017-04-23 10:19:03)
# 5 => cachedir.item(@=/tmp/cachdir_demo/item_PAMVsM, $=2017-04-23 10:19:03)
# 6 => cachedir.item(@=/tmp/cachdir_demo/item_PXJHQc, $=2017-04-23 10:19:03)
# 7 => cachedir.item(@=/tmp/cachdir_demo/item_G2BD8I, $=2017-04-23 10:19:03)
# 8 => cachedir.item(@=/tmp/cachdir_demo/item_I0osXo, $=2017-04-23 10:19:04)
# 9 => cachedir.item(@=/tmp/cachdir_demo/item_y4n1be, $=2017-04-23 10:19:04)
# 10 => cachedir.item(@=/tmp/cachdir_demo/item_Baa6kF, $=2017-04-23 10:19:04)
# 11 => cachedir.item(@=/tmp/cachdir_demo/item_s1yQFP, $=2017-04-23 10:19:05)
# 12 => cachedir.item(@=/tmp/cachdir_demo/item_J1aTD8, $=2017-04-23 10:19:06)
# 13 => cachedir.item(@=/tmp/cachdir_demo/item_z6g2k3, $=2017-04-23 10:19:06)
# 14 => cachedir.item(@=/tmp/cachdir_demo/item_Q8IDHU, $=2017-04-23 10:19:07)
# Items with name == "foo"
# 0 => cachedir.item(@=/tmp/cachdir_demo/item_9RKElJ, $=2017-04-23 10:19:02)
# 1 => cachedir.item(@=/tmp/cachdir_demo/item_1cRfSy, $=2017-04-23 10:19:02)
# 2 => cachedir.item(@=/tmp/cachdir_demo/item_30XOSW, $=2017-04-23 10:19:02)
# 3 => cachedir.item(@=/tmp/cachdir_demo/item_PAMVsM, $=2017-04-23 10:19:03)
# 4 => cachedir.item(@=/tmp/cachdir_demo/item_PXJHQc, $=2017-04-23 10:19:03)
# Items with even "iter"
# 0 => cachedir.item(@=/tmp/cachdir_demo_cache/item_9RKElJ, $=2017-04-23 10:19:02)
# 1 => cachedir.item(@=/tmp/cachdir_demo_cache/item_S1FVBg, $=2017-04-23 10:19:02)
# 2 => cachedir.item(@=/tmp/cachdir_demo_cache/item_30XOSW, $=2017-04-23 10:19:02)
# 3 => cachedir.item(@=/tmp/cachdir_demo_cache/item_PXJHQc, $=2017-04-23 10:19:03)
# 4 => cachedir.item(@=/tmp/cachdir_demo_cache/item_G2BD8I, $=2017-04-23 10:19:03)
# 5 => cachedir.item(@=/tmp/cachdir_demo_cache/item_y4n1be, $=2017-04-23 10:19:04)
# 6 => cachedir.item(@=/tmp/cachdir_demo_cache/item_Baa6kF, $=2017-04-23 10:19:04)
# 7 => cachedir.item(@=/tmp/cachdir_demo_cache/item_J1aTD8, $=2017-04-23 10:19:06)
# 8 => cachedir.item(@=/tmp/cachdir_demo_cache/item_Q8IDHU, $=2017-04-23 10:19:07)
