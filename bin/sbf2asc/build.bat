Rem Batch script to compile "sbf2asc" with the
Rem Microsoft Visual C++ Compiler
Rem (c) 2000-2016 Copyright Septentrio NV/SA. All rights reserved.


cl -Ox -DNO_DECRYPTION -EHsc sbf2asc.c sbfread.c sbfread_meas.c sbfsvid.c ssngetop.c crc.c mscssntypes.c
