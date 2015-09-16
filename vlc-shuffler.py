import sys
import random
import os
import xml.etree.ElementTree as ElementTree


def shuffle(items):
    """
    In-place shuffle of a list

    Args:
        items: The list to be shuffled
    """
    for i in range(len(items)):
        a = items[i]
        rand_i = random.randint(0, len(items)-1)
        b = items[rand_i]
        a, b, = b, a
        items[i] = a
        items[rand_i] = b

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " [playlist1] [playlist2] ...")
        sys.exit()

    for i in range(1, len(sys.argv)):
        ET = ElementTree.parse(sys.argv[i])
        root = ET.getroot()
        ns0 = ''  # namespace0
        ns1 = ''  # namespace1

        # Find out what the namespace strings are
        for item in root.iter():
            if 'track' in item.tag:
                trackBegin = item.tag.rfind('track')
                ns0 = item.tag[0:trackBegin]
                break
        for item in root.iter():
            if 'id' in item.tag:
                idBegin = item.tag.rfind('id')
                ns1 = item.tag[0:idBegin]
                break

        # Get a list of ids for each track
        track_ids = []
        for track in root.iter(ns0+'track'):
            extension = track.find(ns0+'extension')
            tid = extension.find(ns1+'id')
            track_ids.append(tid.text)

        shuffle(track_ids)

        # Replace each original track id with a shuffled id
        trackList = root.find(ns0+'trackList')
        orig_track_ids = trackList.iter(ns1+'id')      
        for orig, shuffled_id in zip(orig_track_ids, track_ids):
            orig.text = shuffled_id

        # Output to file
        name, ext = os.path.splitext(sys.argv[i])
        output_name = name + '_shuffled' + ext
        ET.write(
            output_name,
            xml_declaration=True,
            )

        # Still need to replace the namespaces
        # with the proper values. ElementTree is kinda buggy when
        # it comes to namespaces, so do it by hand.
        data = ''
        with open(output_name, 'rt') as fp:
            data = fp.read()
            ns0 = ns0.replace('{', '')
            ns0 = ns0.replace('}', '')
            ns1 = ns1.replace('{', '')
            ns1 = ns1.replace('}', '')

            print(ns0, ns1)
            data = data.replace('ns0:', '')
            data = data.replace('ns1:', 'vlc:')
        with open(output_name, 'wt') as fp:
            fp.write(data)

            
        
