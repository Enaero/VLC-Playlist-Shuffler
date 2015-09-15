import sys
import random
import xml.etree.ElementTree as ElementTree


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " [playlist1] [playlist2] ...")
        sys.exit()

    for i in range(1, len(sys.argv)):
        ET = ElementTree.parse(sys.argv[i])
        root = ET.getroot()
        print(root[1][0][0].text)


