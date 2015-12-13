import os
import argparse
import requests


video_file_formats = {
    '.wmv',
    '.webm',
    '.vob',
    '.gifv',
    '.svi',
    '.roq',
    '.rmvb',
    '.rm',
    '.yuv',
    '.mov',
    '.qt',
    '.ogv',
    '.ogg',
    '.nsv',
    '.mng',
    '.mp4',
    '.m4p',
    '.m4v',
    '.mpg',
    '.mpeg',
    '.m2v',
    '.mp2',
    '.mpe',
    '.mpv',
    '.mkv',
    '.mxf',
    '.m4v',
    '.flv',
    '.f4v',
    '.f4p',
    '.f4a',
    '.f4b',
    '.drc',
    '.avi',
    '.asf',
    '.3g2',
    '.3gp',
}

if __name__ != '__main__':
    raise ValueError("u stupee")

parser = argparse.ArgumentParser(
        description=('Crawls dirs in search of video files and compiles'
                     'them into a playlist')
        )
parser.add_argument('-o', '--output', metavar='output', type=str, nargs=1)
parser.add_argument('roots', metavar='ROOT_PATHS', type=str, nargs='+',
                    help='Source directories for crawling')
args = parser.parse_args()

print("Got these arguments: {}".format(args))
print("Scanning . . .")
playlist = []
for root in args.roots:
    if not os.path.isabs(root):
        raise ValueError("All source dirs must be absolute paths. "
                         "example: 'C:\\' NOT 'C:'")

    for path, folders, files in os.walk(root):
        for name in files:
            base, ext = os.path.splitext(name)
            if ext not in video_file_formats:
                continue
            full_name = os.path.join(path, name)
            playlist.append(full_name)

print("Found {} video files.".format(len(playlist)))
      
with open(args.output[0], 'wt') as fp:
    for path in playlist:
        path = path.replace('\\', '/')
        path = 'file:///' + requests.utils.quote(path)
        fp.write(path + '\n')

print("Written to", args.output[0])
            
