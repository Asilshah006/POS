from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pymongo import MongoClient
Builder.load_file('Signin.kv')

class SignInWindow(BoxLayout):
    def __init__(self , **kwargs):
        super().__init__(**kwargs)
        client = MongoClient()
        self.db = client.Test
        self.users = self.db.users


    def validate_user(self):

        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info_label

        userN = user.text
        passW = pwd.text

        user.text = ''
        pwd.text = ''

        if(userN == '' and passW == ''):
            info.text = '[color=#FF0000]Please Enter Username and Password First[/color]'
        else:
            user = self.users.find_one({'User_Name' : userN})
            if user == None:
                info.text = '[color=#FF0000]Invalid Username or Password[/color]'

            else:
                if passW == user['Password']:
                    des = user['Designation']
                    if des == 'Administrator':
                        # info.text = '[color=#00FF00]Logged in Successfully[/color]'
                        self.parent.parent.current = 'scrn_admin'
                    else:
                        self.parent.parent.parent.ids.scrn_op.children[0].ids.loggedin_user.text = str.upper(userN)
                        self.parent.parent.current = 'scrn_op'

                else:
                    info.text = '[color=#FF0000]Invalid Username or Password[/color]'


class SigninApp(App):
     def build(self):
         return SignInWindow()


if __name__ == "__main__":
    sa = SigninApp()
    sa.run()