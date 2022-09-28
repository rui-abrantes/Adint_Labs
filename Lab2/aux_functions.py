#!/usr/bin/env python3

from hashlib import new


def count_letter(msg):
    my_dict = {}
    for i in range(len(msg)):
        if msg[i] in my_dict:
            my_dict[msg[i]] += 1
        elif msg[i].isdigit():
            continue   
        else:
            my_dict[msg[i]] = 1
    print(my_dict)
    return my_dict

def count_digit(msg):
    my_dict = {}
    for i in range(len(msg)):
        if msg[i].isdigit():
            if msg[i] in my_dict:
                my_dict[msg[i]] += 1 
            else:
                my_dict[msg[i]] = 1
    print(my_dict)
    return my_dict
