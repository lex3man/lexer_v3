from django.http import JsonResponse
from django.views import View
from .handler import GetUser, GetUsers_info, CreateUser
from core.auth_check import auth_pass

import json

class UserController(View):

    @auth_pass
    def get(self, request):
        '''
        Запрос информации о пользователе или группе пользователей
        По telegram id : ?head=telegramid&tgid=<ID>
        По логину в системе : ?head=login&login=<LOGIN>
        С фильтрацией по проекту/группе/тэгу : ?head=userfilters&ft=pgt&p_id=<ID>&g_id=<ID>&t_id=<ID>
        '''
        
        data = {"status":"error"}
        data.update({
            "security":"auth passed",
            "msg":"wrong request"
        })
        head = request.GET.get('head')
        
        # все пользователи
        if head == 'all_users':
            response_data = GetUsers_info.with_filters()

        elif head == 'telegramid':
            user = GetUser.fromTelegram(request.GET.get('tgid'))
            response_data = user.printInfo()
        
        elif head == 'login':
            user = GetUser.fromWeb(request.GET.get('login'))
            response_data = user.printInfo()
        
        elif head == 'userfilters':
            match request.GET.get('ft'):
                # запрос фильтрации по проекту
                case 'p': 
                    filters_data = {
                        'group_id':'all',
                        'tag_id':'all',
                        'proj_id':request.GET.get('p_id')
                    }
                # запрос фильтрации по группе
                case 'g': 
                    filters_data = {
                        'group_id':request.GET.get('g_id'),
                        'tag_id':'all',
                        'proj_id':'all'
                    }
                # запрос фильтрации по тэгу
                case 't': 
                    filters_data = {
                        'group_id':'all',
                        'tag_id':request.GET.get('t_id'),
                        'proj_id':'all'
                    }
                # запрос фильтрации по проекту и группе
                case 'pg': 
                    filters_data = {
                        'group_id':request.GET.get('g_id'),
                        'tag_id':'all',
                        'proj_id':request.GET.get('p_id')
                    }
                # запрос фильтрации по проекту и тэгу
                case 'pt': 
                    filters_data = {
                        'group_id':'all',
                        'tag_id':request.GET.get('t_id'),
                        'proj_id':request.GET.get('p_id')
                    }
                # запрос фильтрации по группе и тэгу
                case 'gt': 
                    filters_data = {
                        'group_id':request.GET.get('g_id'),
                        'tag_id':request.GET.get('t_id'),
                        'proj_id':'all'
                    }
                # запрос фильтрации по проекту, группе и тэгу
                case 'pgt': 
                    filters_data = {
                        'group_id':request.GET.get('g_id'),
                        'tag_id':request.GET.get('t_id'),
                        'proj_id':request.GET.get('p_id')
                    }
            response_data = GetUsers_info.with_filters(filters_data)
        
        data.update({
            "status":"OK",
            "msg":"query_passed",
            "answer":response_data
        })
        return JsonResponse(data)
    
    @auth_pass
    def put(self, request):
        '''
        Запрос на создание нового пользователя
        '''
        data = {"status":"error"}
        data.update({
            "security":"auth passed",
            "msg":"wrong request"
        })
        put_body = json.loads(request.body)
        
        if put_body['src'] == 'telegram':
            new_user = CreateUser.fromTelegram(
                bot_name = put_body['bot_name'],
                telegramID = put_body['telegid'],
                firstName = put_body['firstName'],
                lastName = put_body['lastName'],
                nickName = put_body['nickName']
            )
        elif put_body['src'] == 'web':
            new_user = CreateUser.fromWeb(
                projectID = put_body['project_id'],
                firstName = put_body['firstName'],
                lastName = put_body['lastName'],
                login = put_body['login'],
                passwd = put_body['passwd']
            )
        data.update({
            "msg":f"New user '{put_body['firstName']} {put_body['lastName']}' is created"
        })
            
        new_user.save()
        
        return JsonResponse(data)
    
    @auth_pass
    def post(self, request):
        '''
        Запрос на изменение информации о пользователе
        '''
        data = {"status":"error"}
        data.update({
            "security":"auth passed",
            "msg":"wrong request"
        })
        post_body = json.loads(request.body)
        
        # Изменение пользователей
        
        return JsonResponse(data)