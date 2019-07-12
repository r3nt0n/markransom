#!/usr/bin/env python
# -*- coding: utf-8 -*-
# M4rk.R4NS0M [decipher]
# R3nt0n 11/2016

import os
import argparse
from base64 import b64decode

from Crypto.Cipher import AES

from ransompy import findRootPaths, findFiles


def decipher(cipherData, key):
    iv = (cipherData.split(':%:%:&:%:%:'))[0]
    cipherText = (cipherData.split(':%:%:&:%:%:'))[1]
    decipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decipherData = decipher.decrypt(cipherText)
    decipherData = b64decode(decipherData)
    return decipherData


###############################################################################
# PROCESAMIENTO DE ARGUMENTOS PASADOS AL EJECUTAR EL SCRIPT
###############################################################################
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description='Decrypt files encrypted with the \
                                              M4rk.R4NS0M script.')

# Definición de todos los argumentos
parser.add_argument('-k', '--key', action="store", metavar='file', type=str,
                    dest='key', required=True,
                    help='Indicates the file which includes the key. \
                          The key has to be encoded in base64.')

parser.add_argument('-f', '--file', action="store", metavar='file', type=str,
                    dest='file', default='*.mrcrypt',
                    help='specifies file to decrypt. If not specifies, the \
                          script will search for all the files with the .cript \
                          extension.')

# Recogida en variables de cada argumento (referenciados por atributo dest)
args = parser.parse_args()

key = args.key
cryptedFile = args.file
###############################################################################

# Decrypt all the files
if cryptedFile == '*.mrcrypt':
    rootPaths = findRootPaths()
    fileList = findFiles(rootPaths, '.mrcrypt', 'non_excluded_mps')
    # Desencriptamos los ficheros
    for cryptedFile in fileList:
        try:
            with open(cryptedFile, 'rb') as fCrypt:
                cipherData = fCrypt.read()
            data = decipher(cipherData, key)
            prevName = cryptedFile[:-6]
            with open(prevName, 'wb+') as fPlain:
                fPlain.write(cipherData)
            os.remove(cryptedFile)
        except:
            pass

# Decrypts only the file specified by the --file argument
else:
    try:
        with open(cryptedFile, 'rb') as fCrypt:
            cipherData = fCrypt.read()
        data = decipher(cipherData, key)
        prevName = cryptedFile[:-6]
        with open(prevName, 'wb+') as fPlain:
            fPlain.write(cipherData)
        os.remove(cryptedFile)
    except:
        pass
