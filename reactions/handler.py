from bots.models import TelegramBot
from .models import Command, Answer

bot_handler = {}

class Reaction:
    
    def __init__(self, resp_type: str, content: str, delay: int, keyboard: dict, bot_id: str):
        self.type = resp_type
        self.content = content
        self.delay = delay
        self.keyboard = keyboard
        self.bot = TelegramBot.objects.get(tg_id = bot_id)
    
    @classmethod
    def get_reaction(cls, req_type: str, content: str, bot_id: str):
        
        if req_type == 'command':
            cmd = Command.objects.filter(bot__tg_id = bot_id).get(caption = content)
            try:
                kb = cmd.keyboard
                buttons_data = {}
                for btn in kb.buttons.all():
                    buttons_data.update({
                        btn.caption:{
                            'text':btn.text,
                            'order':btn.order
                        }
                    })
                kb_data = {
                    'type':kb.type,
                    'caption':kb.caption,
                    'buttons':buttons_data
                }
            except: kb_data = {'type':'None'}
            tg_bot = cls('text', cmd.text, cmd.delay, kb_data, bot_id)
            bot_handler.update({bot_id:tg_bot})
            return tg_bot