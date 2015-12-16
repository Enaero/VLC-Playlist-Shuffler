import argparse
import os
import xml.etree.ElementTree as ET
from datetime import date
import time
import random
import pathlib

if __name__ != '__main__':
    raise ValueError("u stupee")


def jank_parse(file_name, result):
    with open(file_name, 'rt') as fp:
        line = fp.readline()
        while line:
            loc_begin = line.find('<location>', 0)
            loc_end = line.find('</location>', loc_begin + 1)
            while loc_begin >= 0 and loc_end >= 0:
                text_start = line.find('>', loc_begin + 1) + 1
                text_end = line.find('<', text_start)
                text = line[text_start:text_end]
                result.append(text)
                loc_begin = line.find('<location>', loc_begin + 1)
                loc_end = line.find('</location>', loc_begin + 1)
            line = fp.readline()


def shuffle(items, start=0, end=None):
    if start >= len(items):
        return
    if not end or end > len(items):
        end = len(items)

    length = end - start
    for i in range(length):
        j = random.randint(0, length-1)
        a = items[start + i]
        b = items[start + j]
        items[start + i], items[start + j] = b, a


def main(playlists):
    result = list()
    for playlist in playlists:
        print('Doing {}'.format(playlist))
        if playlist.endswith('.m3u'):
            print(
                '{}: We only use .m3u8 or .xspf here (unicode!)'
                  .format(playlist)
            )
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
                try:
                    jank_parse(playlist, result)
                    continue
                except Exception:
                    print('Could not parse {}.'.format(playlist))
                    continue
            root = tree.getroot()
            prev_len = len(result)
            for item in root.iter():
                if item.tag.endswith('location'):
                    result.append(item.text)
            if len(result) == prev_len:
                print('Could not find paths in {}, make sure its .xspf'
                       .format(playlist))
        elif os.path.isdir(playlist):
            for path, folders, files in os.walk(playlist):
                for file in files:
                    full = os.path.join(path, file)
                    result += main([full])
                for folder in folders:
                    full = os.path.join(path, folder)
                    result += main([full])
        else:
            print('Can\'t do {}'.format(playlist))
    print('Adding {} to result'.format(len(result)))
    return result


cmd_parser = argparse.ArgumentParser(description='shuffle playlists')
cmd_parser.add_argument('playlists', metavar='playlists', type=str, nargs='+',
                        help='list of playlists to string together')
cmd_parser.add_argument('--noshuffle', action='store_true',
                        help='Instead of shuffling, will noshuffle the lists')
cmd_parser.add_argument('--output', metavar='OUTPUT_NAME', type=str, nargs=1,
                        help='Name of output file (optional)')
cmd_parser.add_argument('--filters', metavar='FILTERS', type=str, nargs='+',
                        help=('Paths won\'t be added unless they start with one'
                             'of these paths'))
cmd_parser.add_argument('--radius', '-r', metavar='SHUFFLE_RADIUS', type=int,
                        nargs=1, help='How far away an item can be shuffled')
args = cmd_parser.parse_args()
print('Got these args {}'.format(args))

result = list(main(args.playlists))

if not args.noshuffle:
    if args.radius:
        radius = args.radius[0]
        print("Shuffling subsections of {}".format(radius))
        for i in range(len(result)//radius + 1):
            start = i * radius
            end = (i + 1) * radius
            shuffle(result, start, end)
    else:
        shuffle(result)

output_name = args.output
if not output_name:
    today = date.today()
    month = today.strftime('%B')
    today = month[0:3] + today.strftime('-%d-%y')
    output_name = "{}_{}_shuffled.m3u8".format(today, int(time.time())%86400)
else:
    output_name = output_name[0]

print("Writing . . .")
count = 0
with open(output_name, 'wt') as fp:
    for path in result:
        skip = False
        if args.filters:
            skip = True
            for filt in args.filters:
                if path.startswith(filt):
                    skip = False
        if not skip:
            fp.write(path + '\n')
            count += 1
if args.filters:
    print('Skipped {} because they didn\'t pass the filter'
          .format(len(result) - count))
print('Written to', output_name)
