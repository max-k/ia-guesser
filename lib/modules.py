# -*- coding: utf-8 -*-

def checkModule(modulename):
    try:
        __import__(modulename)
    except ImportError:
        return False
    return True

