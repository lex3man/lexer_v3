import subprocess, os, redis, signal, weakref
from core.auth_check import get_token, drop_token
from collections import defaultdict

active_bots = {}
bots_status = redis.Redis(db=1)
bot_processes = redis.Redis(db=2)
controller_script = '/home/master/www/www.fountcore.tech/dev/lexer_v3/bots/telegram_bot_controller/bot_app.py'

class ActiveTelegramBot:
    __refs__ = defaultdict(list)
    def __init__(self):
        self._status = 'off'
        self._authToken = ''
        self.__refs__[self.__class__].append(weakref.ref(self))
        
    @classmethod
    def get_instances(cls):
        '''
        Получение экземпляров
        '''
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst
    
class BotHandler(ActiveTelegramBot):
    
    def __init__(self, token: str, bot_caption: str):
        super(BotHandler, self).__init__()
        self._name = bot_caption
        self.__token = token
        bots_status.mset({self._name:'off'})
    
    def __str__(self):
        return f'{self._name} ({self.__token})'
    
    def start_aiogram_app(self):
        '''
        Запуск телеграм бота
        '''
        self._status = bots_status.get(self._name).decode("utf-8")
        if self._status == 'off':
            self._status = 'on'
            token = get_token()
            self._authToken = token.key
            bots_status.mset({self._name:'on'})
            bot_process = subprocess.Popen(['python', controller_script, self.__token, token.key])
            bot_processes.mset({self._name:bot_process.pid})
            print(bot_processes.get(self._name))
        print(f'{self._name} is {bots_status.get(self._name).decode("utf-8")}')

    def bot_down(self):
        '''
        Остановка бота по экземпляру класса
        '''
        self._status = bots_status.get(self._name).decode("utf-8")
        if self._status == 'on':
            self._status = 'off'
            bots_status.mset({self._name:'off'})
            os.kill(int(bot_processes.get(self._name)), signal.SIGKILL)
            bot_processes.mset({self._name:'None'})
            drop_token(self._authToken)
        print(f'{self._name} is {bots_status.get(self._name).decode("utf-8")}')
    
    @staticmethod
    def kill(bot_name: str):
        '''
        остановка бота по названию (передаётся строковой параметр и названием бота bot_name: str)
        '''
        try: os.kill(int(bot_processes.get(bot_name)), signal.SIGKILL)
        except: print('Have no such process')
        bot_processes.mset({bot_name:'None'})
        bots_status.mset({bot_name:'off'})
        print(f'{bot_name} is {bots_status.get(bot_name).decode("utf-8")}')