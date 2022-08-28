from ast import Delete
from bearer_auth.models import AccessToken
from django.http import JsonResponse
from rest_framework import authentication
from functools import wraps
from django.contrib.auth.models import User

def find_token(auth_header):
    if not auth_header:
        return False
    if len(auth_header) == 1:
        return False
    elif len(auth_header) > 2:
        return False
    try:
        token = auth_header[1].decode('utf-8')
        AccessToken.objects.get(key = token)
        return True
    except: return False
    
def auth_pass(func):
    '''
    Декоратор проверки токена аутентификации @auth_pass
    '''
    @wraps(func)
    def wrap(*args):
        data = {"status":"error"}
        if not find_token(authentication.get_authorization_header(args[1]).split()): 
            data.update({"security":"auth failed"})
            return JsonResponse(data)
        return func(*args)
    return wrap

def get_token():
    '''
    Генерирует токены для ботов
    '''
    user = User.objects.get(username = 'lex3man')
    token = AccessToken.objects.create(user = user)
    return token

def drop_token(key):
    token = AccessToken.objects.get(key = key)
    token.delete()