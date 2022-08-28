from django.http import JsonResponse
from django.views import View
from core.auth_check import auth_pass
from reactions.handler import Reaction
from bots.models import TelegramBot

import json

class FeelAction(View):
    
    @auth_pass
    def post(self, request):
        data = {"status":"error"}
        post_body = json.loads(request.body)
        try: TelegramBot.objects.get(tg_id = post_body['bot_id'])
        except: 
            bot = TelegramBot.objects.get(token = post_body['bot_token'])
            bot.tg_id = post_body['bot_id']
            bot.save()
        
        response = Reaction.get_reaction(post_body['type'], post_body['content'], post_body['bot_id'])
        try:
            data.update({
                "status":"OK",
                "response":{
                    "type":response.type,
                    "content":response.content,
                    "delay":response.delay,
                    "keyboard":response.keyboard
                }
            })
        except: data.update({"msg":"Some shit with response"})
        
        return JsonResponse(data)