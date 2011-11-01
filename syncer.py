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
    changes = {}
    for fn in os.listdir(syncdir):
        m = re.match(changes_re, fn)
        if m:
            cur = m.group('cur')
            changes[cur] = m.groupdict()
            changes[cur].update(fn=fn)

    with open(state) as processed:
        processed_so_far = processed.readlines()
        if len(processed_so_far) == 0:
			for change in changes:
				if change['fn'].startswith('00000000000000'):
					next_hash = change['next']
					break
        else:
            next_hash = processed_so_far[-1].rstrip('\n')

    with open(state, 'a') as processed:
        next_hash = changes[next_hash]['next']
        while next_hash in changes:
            process_file(changes[next_hash]['fn'])
            processed.write(next_hash+'\n')
            next_hash = changes[next_hash]['next']
        
