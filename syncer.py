#!/usr/bin/env python
import os
import re
import zipfile

syncdir = '/var/www/dav/OmniFocus.ofocus'
state = 'processed.state'
changes_re = re.compile('(?P<ts>\d{14})=(?P<cur>[\w-]+)\+(?P<next>[\w-]+).zip')

def process_file(fn):
    zf = zipfile.ZipFile(os.path.join(syncdir, fn))
    print zf.read('contents.xml')


if __name__ == '__main__':
    # dict of cur -> next
    changes = {}
    timestamps = {}
    filenames = {}
    for fn in os.listdir(syncdir):
        m = re.match(changes_re, fn)
        if m:
            ts = m.group('ts')
            cur = m.group('cur')
            next = m.group('next')
            changes[cur] = next
            timestamps[cur] = ts
            filenames[cur] = fn

    with open(state) as processed:
        processed_so_far = processed.readlines()
        if len(processed_so_far) == 0:
            for fn in filenames.values():
                if fn.startswith('00000000000000'):
                    m = re.match(changes_re, fn)
                    next_hash = m.group('cur')
                    break
        else:
            next_hash = processed_so_far[-1].rstrip('\n')

    with open(state, 'a') as processed:
        while next_hash in changes:
            process_file(filenames[next_hash])
            #processed.write(next_hash+'\n')
            next_hash = changes[next_hash]
        
