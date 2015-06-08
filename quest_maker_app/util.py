from Crypto.Cipher import AES
import os

from django.conf import settings

ENCRYPTION_KEY = settings.ENCRYPTION_KEY
INIT_VECTOR = settings.INIT_VECTOR


def encrypt(string):
    obj = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, INIT_VECTOR)
    return obj.encrypt(string)


def decrypt(string):
    obj = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, INIT_VECTOR)
    return obj.decrypt(string)