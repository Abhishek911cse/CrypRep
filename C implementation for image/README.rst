
Compilation & Installation
==========================


1. Make sure des.c, des.h and run_des.c are in the same directory 
2. Compile using: gcc -O3 des.c run_des.c -o run_des.o   

Usage
=====
Say we want to encrypt/ decrypt a file named /home/user/sample.txt

1. Generate a keyfile using::

    run_des.o -g /tmp/keyfile.key
2. Encrypt sample.txt using::

    run_des.o -e /tmp/keyfile.key /home/user/sample.txt /home/user/sample.enc
3. Decrypt sample.txt using::

    run_des.o -d /tmp/keyfile.key /home/user/sample.enc /home/user/sample_decrypted.txt

Don't lose the key file! you won't be able to decrypt an encrypted if you lose the keyfile.

