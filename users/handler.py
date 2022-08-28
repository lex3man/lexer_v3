from .models import UserData, SystemUser, TelegramUser, PersonalInfo
from bots.models import TelegramBot
from classificators.models import Project
from collections import defaultdict
import random, string, weakref

def idGenerate(lenght: int):
    '''
    Генератор ID пользователей
    '''
    while True:
        sights = string.digits + string.ascii_lowercase
        code = ''.join(random.choices(sights, k = lenght))
        if UserData.objects.filter(uID = code).count() == 0: break
    return code

class User:
    __refs__ = defaultdict(list)
    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst

class CreateUser(User):
    '''
    Интерфейс регистрации пользователей
    '''
    
    def __init__(self, data: dict):
        super(CreateUser, self).__init__()
        self.__uID = idGenerate(8)
        self.__userFirstName = data['firstName']
        self.__userLastName = data['lastName']
        self.__email = 'not set'
        if data['from'] == 'telegram':
            self.__userTelegramID = data['telegramID']
            self.__nickName = data['nickName']
            self.__fromBot = data['bot_name']
        if data['from'] == 'web':
            self.__login = data['login']
            self.__passwd = data['passwd']
            self.__projectID = data['projectID']

    @classmethod
    def fromTelegram(cls, bot_name: str, telegramID: str, firstName: str, lastName: str, nickName: str):
        '''
        Регистрация пользователя через телеграм
        '''
        data = {
            'from':'telegram',
            'bot_name':bot_name,
            'firstName':firstName,
            'lastName':lastName,
            'telegramID':telegramID,
            'nickName':nickName
        }
        return cls(data)
    
    @classmethod
    def fromWeb(cls, projectID: str, firstName: str, lastName: str, login: str, passwd: str):
        '''
        Регистрация пользователя через сайт
        '''    
        data = {
            'from':'web',
            'projectID':projectID,
            'firstName':firstName,
            'lastName':lastName,
            'login':login,
            'passwd':passwd
        }
        return cls(data)
    
    def save(self):
        '''
        Запись пользователя в базу данных
        '''
        usr = UserData(
            uID = self.__uID,
            uFirstName = self.__userFirstName,
            uLastName = self.__userLastName,
            uFullName = f'{self.__userFirstName} {self.__userLastName}',
            uEmail = self.__email
        )
        usr.save()
        from_project = None
        try:
            TgData = TelegramUser(
                keyUser = usr,
                uNickName = self.__nickName,
                uTelegramID = self.__userTelegramID
            )
            TgData.save()
            bot = TelegramBot.objects.get(caption = self.__fromBot)
            from_project = bot.project
        except: pass
        try:
            SystemData = SystemUser(
                keyUser = usr,
                uLogin = self.__login,
                uPasswd = self.__passwd
            )
            SystemData.save()
            from_project = Project.objects.get(id = self.__projectID)
        except: pass
        usr.from_project = from_project
        usr.save()


class GetUser(User):
    '''
    Интерфейс получения информации о пользователе
    '''
    def __init__(self, from_src: str, uID: str):
        super(GetUser, self).__init__()
        match from_src:
            case 'telegram': 
                userTD = TelegramUser.objects.get(uTelegramID = uID)
                user = userTD.keyUser
                self.__userTelegramID = uID
                self.__nickName = userTD.uNickName
            case 'web':
                userWeb = SystemUser.objects.get(uLogin = uID)
                user = userWeb.keyUser
                self.__login = uID
        self.__uID = user.uID
        self.__userFirstName = user.uFirstName
        self.__userLastName = user.uLastName
        self.__email = user.uEmail
        try:
            info = PersonalInfo.objects.get(keyUser = user)
            self.__userGender = info.uGender
            self.__userPhone = info.uPhoneNumber
        except:
            self.__userGender = 'not set'
            self.__userPhone = 'not set'

    @classmethod
    def fromTelegram(cls, uTgID: str):
        '''
        запрос пользователя по ID Telegram
        '''
        try:
            TelegramUser.objects.get(uTelegramID = uTgID)
            print('Telegram data was found')
            return cls('telegram', uTgID)
        except:
            print ('No such user')
            return None
    
    @classmethod
    def fromWeb(cls, login: str):
        '''
        запрос пользователя по логину WEB system
        '''
        try:
            SystemUser.objects.get(uLogin = login)
            print('Web data was found')
            return cls('web', login)
        except:
            print ('No such user')
            return None
    
    def printInfo(self):
        '''
        формирование словаря с данными о пользователе
        '''
        data = {
            'ID':self.__uID,
            'First Name':self.__userFirstName,
            'Last Name':self.__userLastName,
            'Full Name':f'{self.__userFirstName} {self.__userLastName}',
            'Email':self.__email
        }
        user = UserData.objects.get(uID = self.__uID)
        
        # добавление личной информации
        try:
            PersonalInfo.objects.get(keyUser = user)
            data.update({
                'Personal Info':{
                    'Gender':self.__userGender,
                    'Phone Number':self.__userPhone
                }
            })
        except: data.update({'Personal Info':'None'})
        
        # добавление информации об акаунте в телеграм
        try:
            TelegramUser.objects.get(keyUser = user)
            data.update({
                'Telegram Data':{
                    'ID':self.__userTelegramID,
                    'Nick Name':self.__nickName
                }
            })
        except: data.update({'Telegram Data':'None'})
        
        # добавление информации об учётной записи в системе
        try:
            SystemUser.objects.get(keyUser = user)
            data.update({
                'System Data':{
                    'Login':self.__login
                }
            })
        except: data.update({'System Data':'None'})

        return data


class GetUsers_info:
    '''
    Интерфейс получения информации о пользователях
    '''
    filters = {
        'group_id':'all',
        'tag_id':'all',
        'proj_id':'all'
    }
    
    @classmethod
    def with_filters(cls, uQuery: dict = filters):
        users = UserData.objects.all()
        
        # Фильтрация пользователей
        try:
            if uQuery['proj_id'] != 'all': 
                users = users.filter(from_project__id = uQuery['proj_id'])
            if uQuery['group_id'] != 'all': 
                users = users.filter(groups__id = uQuery['group_id'])
            if uQuery['tag_id'] != 'all': 
                users = users.filter(tags__id = uQuery['tag_id'])
            resp = 'There are no such users'
        except: resp = 'filter error'
        
        data = {'Query':uQuery, 'response':resp}
        for usr in users:
            info = {}
            for field in UserData._meta.fields:
                info.update({field.name:getattr(usr, field.name).__str__()})
            usersData = {usr.uID:info}
            data.update({'response':usersData})
        return data