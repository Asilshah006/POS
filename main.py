from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from signin import SignInWindow
from operator_pack.Operator import OperatorWindow
from admin_pack.admin import AdminWindow

class MainWindow(BoxLayout):

    signin = SignInWindow()
    admin_win = AdminWindow()
    operator_win = OperatorWindow()


    def __init__(self , **kwargs):
        super().__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin)
        self.ids.scrn_admin.add_widget(self.admin_win)
        self.ids.scrn_op.add_widget(self.operator_win)




class MainApp(App):
    def build(self):
        return MainWindow()


ma = MainApp()
ma.run()
