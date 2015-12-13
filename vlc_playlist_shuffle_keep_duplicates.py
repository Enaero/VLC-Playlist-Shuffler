import argparse
import os
import xml.etree.ElementTree as ET
from datetime import date
import time
import random
import pathlib

if __name__ != '__main__':
    raise ValueError("u stupee")

def shuffle(items):
    length = len(items)
    for i in range(length):
        j = random.randint(0, length-1)
        a = items[i]
        b = items[j]
        items[i], items[j] = b, a


def main(playlists):
    result = []
    for playlist in playlists:
        print('Doing {}'.format(playlist))
        if playlist.endswith('.m3u'):
            raise ValueError('We only use .m3u8 or .xspf here (unicode!)')
        elif playlist.endswith('.m3u8'):
            with open(playlist, 'rt') as fp:
                path = fp.readline().strip()
                while(path):
                    result.append(path)
                    path = fp.readline().strip()
        elif playlist.endswith('.xspf'):
            try:
                tree = ET.parse(playlist)
            except ET.ParseError:
                print('Could not parse {}.'.format(playlist))
                continue
            root = tree.getroot()
            prev_len = len(result)
            for item in root.iter():
                if item.tag.endswith('location'):
                    result.append(item.text)
            if len(result) == prev_len:
                raise ValueError('Could not find paths in {}, make sure its .xspf'
                                 .format(playlist))
        elif os.path.isdir(playlist):
            for path, folders, files in os.walk(playlist):
                for file in files:
                    full = os.path.join(path, file)
                    result.extend(main([full]))
                for folder in folders:
                    full = os.path.join(path, folder)
                    result.extend(main([full]))
        else:
            print('Can\'t do {}'.format(playlist))
    print('Adding {} to result'.format(len(result)))
    return result


cmd_parser = argparse.ArgumentParser(description='noshuffle playlists')
cmd_parser.add_argument('playlists', metavar='playlists', type=str, nargs='+',
                        help='list of playlists to string together')
cmd_parser.add_argument('--noshuffle', action='store_true',
                        help='Instead of shuffling, will noshuffle the lists')
cmd_parser.add_argument('--output', metavar='OUTPUT_NAME', type=str, nargs=1,
                        help='Name of output file (optional)')

args = cmd_parser.parse_args()
print('Got these args {}'.format(args.playlists))

result = main(args.playlists)

if not args.noshuffle:
    shuffle(result)

output_name = args.output
if not output_name:
    today = date.today()
    month = today.strftime('%B')
    today = month[0:3] + today.strftime('-%d-%y')
    output_name = "{}_{}_shuffled.m3u8".format(today, int(time.time())%86400)
else:
    output_name = output_name[0]

with open(output_name, 'wt') as fp:
    for path in result:
        fp.write(path + '\n')
print('Written to', output_name)
