# Author: Farmehr Farhour f.farhour@gmail.com Purpose: The purpose of this
# Purpose: this script will read in the data from a calibre library & copy the
# books into corresponding folders based on the Universal Decimal
# Classification. It uses
# http://classify.oclc.org/classify2/api_docs/classify.html  to classify them
# based on the ISBN

import os,sys,argparse   #built-in

def main(argv):
    # argparse
    parser = argparse.ArgumentParser(description='Process calibre library')
    requiredNamed = parser.add_argument_group('Required Named Arguments')
    requiredNamed.add_argument('--inputLocation', '-i', type=str, metavar='<input location>', help='the input library location', required=True)
    requiredNamed.add_argument('--outputLocation', '-o', type=str, metavar='<output location>', help='the output library location', required=True)
    parser.add_argument('--no-copy', dest='copy', action='store_false', help='choose to not copy the files over.')
    parser.set_defaults(copy=True)

    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main(sys.argv)
