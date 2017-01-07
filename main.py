# Author: Farmehr Farhour f.farhour@gmail.com Purpose: The purpose of this
# Purpose: this script will read in the data from a calibre library & copy the
# books into corresponding folders based on the Universal Decimal
# Classification. It uses
# http://classify.oclc.org/classify2/api_docs/classify.html  to classify them
# based on the ISBN

import os,re,sys,argparse   #built-in
from lxml import html
from lxml import etree as ET
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


    for root, dirs, files in os.walk(args.inputLocation):
        for file in files:
            if re.match("metadata.opf", file):
                print(file)
                tree = ET.parse(os.path.join(root, file))
                xmlroot = tree.getroot()
                # http://stackoverflow.com/questions/14552138/python-elementtree-find-using-a-wildcard
                isbn = xmlroot.xpath(".//*[local-name()='metadata']//*[local-name()='identifier'][@*[local-name()='scheme']='ISBN']/text()")
                for filename in os.listdir(root):
                    if re.match("^.*\.pdf", filename):
                        if(len(isbn)==0):
                            print("METADATA of " + filename + " does not contain an ISBN. The book is skipped.")
                            # break from main loop iteration
                        print isbn
                        print filename

                        r = requests.get('http://classify.oclc.org/classify2/Classify?isbn=' + isbn[0] + '&summary=true')
                        #print(r.text)
                        content = r.text.encode('utf-8')
                        result_root = ET.fromstring(content)
                        classnumber = result_root.xpath(".//*[local-name()='ddc']//*[local-name()='mostPopular']/@sfa")

                        if(len(classnumber)==0):
                            # print(r.status_code)
                            # print(r.text)
                            wi = result_root.xpath(".//*[local-name()='work']/@wi")

                            r = requests.get('http://classify.oclc.org/classify2/Classify?wi=' + wi[0] + '&summary=true')
                            content = r.text.encode('utf-8')
                            result_root = ET.fromstring(content)
                            classnumber = result_root.xpath(".//*[local-name()='ddc']//*[local-name()='mostPopular']/@sfa")

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
