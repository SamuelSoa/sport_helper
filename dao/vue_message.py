# from vue.abstractview import AbstractView
# from vue.abstractview import AbstractView
# from InquirerPy import inquirer
# from InquirerPy.validator import PasswordValidator
# from InquirerPy.base.control import Choice
# from dao.userDAO import UserDAO
# from termcolor import colored
# from pyfiglet import Figlet

# from dao.annonceDAO import AnnonceDAO
# from dao.userDAO import UserDAO

# from vue.session import Session
# from vue.menu2view import Menu2View
# from business_object.particulier import Particulier

# import os

# class Messagevue():
#     def __init__(self):
#         self.qst1 = inquirer.select(
#                         message = f'Gérer la messagerie : '
#                         , choices=[
#                         Choice('Retourner au menu')])

    
#     def display_info(self) : 
#         import os
#         os.system('cls')
#         print(colored(Figlet(font='cybermedium').renderText('Ma messagerie').format('100'),'red'))
#         from dao.MessageDao import MessageDao
#         if MessageDao().get_all_message() != None :
#          from dao.userDAO import UserDAO
#          from dao.MessageDao import MessageDao
#          for ele in MessageDao().get_id() :
#             print('{} : {}'.format(UserDAO().get_prenom_by_id(ele),MessageDao().get_message_by_id_user(ele)))
#         else :
#                 print('Messagerie vide')
#     def make_choice(self):
#         choosed = self.qst1.execute()
#         if choosed == 'Retourner au menu':
#              import os
#              os.system('cls')
#              from vue.menu2view import Menu2View
#              return Menu2View()