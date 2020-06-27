![[Version 1.0](https://github.com/R3nt0n)](http://img.shields.io/badge/version-v1.0-orange.svg)
![[Python 2.7](https://github.com/R3nt0n)](http://img.shields.io/badge/python-2.7-blue.svg)
![[GPL-3.0 License](https://github.com/R3nt0n)](https://img.shields.io/badge/license-GPL%203.0-brightgreen.svg)
![[Date](https://github.com/R3nt0n)](http://img.shields.io/badge/date-2017-yellow.svg)


# markransom

Markransom is a tool created to **encrypt** all the **files** that matches an extension pattern. Can be decrypted with decipher.py and the encryption key generated.

The app will generate an AES256 key and an optional messsage in the desktop. You can configure your own settings in the firsts lines of the script.

This app was **written in 2017**.

## Decipher usage

```
usage: decipher.py [-h] -k file [-e .ext] [-f file]  

Decrypt files encrypted with markransom.py.

optional arguments:
  -h, --help            show this help message and exit
  -k file, --key file   the file which includes the key
  -e .ext, --extension  encrypted files extension
  -f file, --file file  decrypt a single file  
```

## Requirements
+ Python 2.7
+ Pycryptodome


## Legal disclaimer
This tool is created for the sole purpose of security awareness and education, it should not be used against systems that you do not have permission to test/attack. The author is not responsible for misuse or for any damage that you may cause. You agree that you use this software at your own risk. 
