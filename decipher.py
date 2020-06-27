#!/usr/bin/env python
# -*- coding: utf-8 -*-
# markransom.py - decipher
# https://www.github.com/R3nt0n/markransom


import os, sys
import argparse
from base64 import b64decode

from Crypto.Cipher import AES

from markransom import find_root_paths, find_files


def decipher(cipher_data, key):
    iv = (cipher_data.split(':%:%:&:%:%:'))[0]
    cipher_text = (cipher_data.split(':%:%:&:%:%:'))[1]
    d = AES.new(key, AES.MODE_CBC, iv=iv)
    decipher_data = d.decrypt(cipher_text)
    decipher_data = b64decode(decipher_data)
    return decipher_data


def proc_args():
    parser = argparse.ArgumentParser(description='Decrypt files encrypted with markransom.py.')
    parser.add_argument('-k', '--key', action="store", metavar='file',type=str,dest='key', required=True,
                        help='the file which includes the key')
    parser.add_argument('-e', '--extension', action="store", metavar='.ext', type=str, dest='ext',
                        help='Indicates the file which includes the key. The key has to be encoded in base64.')
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
    if not crypted_file:
        root_paths = find_root_paths()
        file_list = find_files(root_paths, e, 'non_excluded_mps')
    else:
        file_list.append(crypted_file)
    # Decrypt each file
    for crypted_file in file_list:
        try:
            with open(crypted_file, 'rb') as f_crypt:
                cipher_data = f_crypt.read()
            data = decipher(cipher_data, key)
            prev_name = crypted_file[:-6]
            with open(prev_name, 'wb+') as f_plain:
                f_plain.write(cipher_data)
            os.remove(crypted_file)
        except:
            pass


if __name__ == '__main__':
    main()