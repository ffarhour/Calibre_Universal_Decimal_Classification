# Author: Farmehr Farhour f.farhour@gmail.com Purpose: The purpose of this
# Purpose: this script will read in the data from a calibre library & copy the
# books into corresponding folders based on the Universal Decimal
# Classification. It uses
# http://classify.oclc.org/classify2/api_docs/classify.html  to classify them
# based on the ISBN

import os,re,sys,argparse   #built-in
import xml.etree.ElementTree as ET
import requests
import codecs

def main(argv):
    # argparse
    parser = argparse.ArgumentParser(description='Process calibre library')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inputLocation', '-i', type=str, metavar='<input location>', help='the input library location', required=True)
    requiredNamed.add_argument('--outputLocation', '-o', type=str, metavar='<output location>', help='the output library location', required=True)
    parser.add_argument('--nocpy', dest='copy', action='store_false', help='choose to not copy the files over.')
    parser.set_defaults(copy=True)

    args = parser.parse_args()
    print(args)


    #xml namespaces
    ns = {  'opf': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'}

    for root, dirs, files in os.walk(args.inputLocation):
        for file in files:
            if re.match("metadata.opf", file):
                print(file)
                tree = ET.parse(os.path.join(root, file))
                xmlroot = tree.getroot()

                for metadata in xmlroot.findall('opf:metadata', ns):
                    for identifier in metadata.findall('dc:identifier[@opf:scheme="ISBN"]', ns):
                        isbn = identifier.text
                        for filename in os.listdir(root):
                            if re.match("^.*\.pdf", filename):
                                print isbn
                                print filename


    r = requests.get('http://classify.oclc.org/classify2/Classify?isbn=0679442723&summary=true')
    print(r.text)
    content = r.text.encode('utf-8')
    result_root = ET.fromstring(content)
    for child in result_root:
        print child.tag, child.attrib

    classnumber = result_root.findall(".//ddc")
    print(classnumber)


                # # Getting rid of namespaces: http://stackoverflow.com/questions/13412496/python-elementtree-module-how-to-ignore-the-namespace-of-xml-files-to-locate-ma
                # tree = ET.iterparse(os.path.join(root, file))
                # for _, el in tree:
                #     if '}' in el.tag:
                #         el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
                # root = tree.root
                # for identifiers in root.iter('identifier'):
                #     print identifiers.attrib
                # # with open(os.path.join(root, file), "r") as metadata:
                # #     for line in metadata:
                # #         print line,

if __name__ == "__main__":
    main(sys.argv)
