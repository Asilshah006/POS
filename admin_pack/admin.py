import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from pymongo import MongoClient
from collections import OrderedDict
from utils.datatable import DataTable
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('admin_pack/admin.kv')

class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (.7, .7)


class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # print(self.get_products())
        # print(self.get_users())
        client = MongoClient()
        db = client.Test
        self.users = db.users
        self.products = db.Products
        self.notify = Notify();

        product_code = []
        product_description = []
        spinvals = []

        for product in self.products.find():
            product_code.append(product['Product_Code'])
            prod_des = product['Product_Description']
            if len(prod_des) > 30:
                prod_des = prod_des[:30] + '....'
            product_description.append(prod_des)

        for i in range(len(product_code)):
            line = ' | '.join([product_code[i], product_description[i]])
            spinvals.append(line)

        self.ids.target_product.values = spinvals

        content = self.ids.scrn_contents
        users = self.get_users()
        usertable = DataTable(table=users)
        content.add_widget(usertable)

        prod_content = self.ids.scrn_product_contents
        products = self.get_products()
        prod_table = DataTable(table=products)
        prod_content.add_widget(prod_table)

    def logout(self):
        self.parent.parent.current = 'scrn_si'
    def kill_switch(self, dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_model = TextInput(hint_text='Model')
        crud_qty = TextInput(hint_text='Qty')
        crud_purchase_p = TextInput(hint_text='Purchase_price')
        crud_sell_p = TextInput(hint_text='sell price')
        crud_last_sale = TextInput(hint_text='last sale')
        crud_before = TextInput(hint_text='before')
        crud_after = TextInput(hint_text='add')
        crud_gen = TextInput(hint_text='gen')
        crud_company = TextInput(hint_text='company')
        crud_submit = Button(text="Add", size_hint_x=None, width=100,
                             on_release=lambda x: self.add_products(crud_code.text, crud_name.text, crud_model.text,
                                                                    crud_qty.text, crud_purchase_p.text,
                                                                    crud_sell_p.text, crud_last_sale.text,
                                                                    crud_before.text, crud_after.text, crud_gen.text,
                                                                    crud_company.text)
                             )
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_model)
        target.add_widget(crud_qty)
        target.add_widget(crud_purchase_p)
        target.add_widget(crud_sell_p)
        target.add_widget(crud_last_sale)
        target.add_widget(crud_before)
        target.add_widget(crud_after)
        target.add_widget(crud_gen)
        target.add_widget(crud_company)
        target.add_widget(crud_submit)

    def add_user_fields(self):

        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text="First Name")
        crud_last = TextInput(hint_text="Last Name")
        crud_user = TextInput(hint_text="User Name")
        crud_password = TextInput(hint_text="Password")
        crud_des = Spinner(text="Operator", values=['Operator', 'Administrator'])
        crud_submit = Button(text="Add", size_hint_x=None, width=100,
                             on_release=lambda x: self.add_users(crud_first.text, crud_last.text, crud_user.text,
                                                                 crud_password.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def add_users(self, first, last, user, passw, des):


        if first == '' or last == '' or user == '' or passw == '' or des == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required [/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            self.users.insert_one(
                {"First_Name": first, "Last_Name": last, "User_Name": user, "Password": passw, "Designation": des,
                 "Date": datetime.datetime.now()})

            content = self.ids.scrn_contents
            content.clear_widgets()
            users = self.get_users()
            usertable = DataTable(table=users)
            content.add_widget(usertable)

    def add_products(self, code, name, model, qty, purchase, sell, l_sale, before, after, gen, company):


        if code == '' or name == '' or model == '' or qty == '' or purchase == '' or sell == '' or l_sale == '' or before == '' or after == '' or gen == '' or company == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields Required [/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            self.products.insert_one(
                {"Product_Code": code, "Product_Description": name, "Model": model, "QTY": qty,
                 "Purchase_Price": purchase,
                 "Sale_Price": sell, "Last_Sale": l_sale, "Before": before, "After": after, "Gen": gen,
                 "Company": company})

            content = self.ids.scrn_product_contents
            content.clear_widgets()
            prod = self.get_products()
            prodtable = DataTable(table=prod)
            content.add_widget(prodtable)

    def update_user_fields(self):

        target = self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text="First Name")
        crud_last = TextInput(hint_text="Last Name")
        crud_user = TextInput(hint_text="User Name")
        crud_password = TextInput(hint_text="Password")
        crud_des = Spinner(text="Operator", values=['Operator', 'Administrator'])
        crud_submit = Button(text="Update", size_hint_x=None, width=100,
                             on_release=lambda x: self.update_users(crud_first.text, crud_last.text, crud_user.text,
                                                                    crud_password.text, crud_des.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_password)
        target.add_widget(crud_des)
        target.add_widget(crud_submit)

    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()

        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_model = TextInput(hint_text='Model')
        crud_qty = TextInput(hint_text='Qty')
        crud_purchase_p = TextInput(hint_text='Purchase_price')
        crud_sell_p = TextInput(hint_text='sell price')
        crud_last_sale = TextInput(hint_text='last sale')
        crud_before = TextInput(hint_text='before')
        crud_after = TextInput(hint_text='add')
        crud_gen = TextInput(hint_text='gen')
        crud_company = TextInput(hint_text='company')
        crud_submit = Button(text="Update", size_hint_x=None, width=100,
                             on_release=lambda x: self.update_products(crud_code.text, crud_name.text, crud_model.text,
                                                                       crud_qty.text, crud_purchase_p.text,
                                                                       crud_sell_p.text, crud_last_sale.text,
                                                                       crud_before.text, crud_after.text, crud_gen.text,
                                                                       crud_company.text)
                             )
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_model)
        target.add_widget(crud_qty)
        target.add_widget(crud_purchase_p)
        target.add_widget(crud_sell_p)
        target.add_widget(crud_last_sale)
        target.add_widget(crud_before)
        target.add_widget(crud_after)
        target.add_widget(crud_gen)
        target.add_widget(crud_company)
        target.add_widget(crud_submit)

    def update_users(self, first, last, user, passw, des):


        if user == '':
                self.notify.add_widget(Label(text='[color=#FF0000][b]User Required[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
        else:
            target_user = self.users.find_one({'User_Name' : user})
            if target_user == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid User[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                if first == '':
                    first = target_user['First_Name']
                if last == '':
                    last = target_user['Last_Name']
                if passw == '':
                    passw = target_user['Password']


                self.users.update_one({"User_Name": user}, {'$set':
                                                            {"First_Name": first, "Last_Name": last, "User_Name": user,
                                                             "Password": passw, "Designation": des,
                                                             "Date": datetime.datetime.now()}})
                content = self.ids.scrn_contents
                content.clear_widgets()

                users = self.get_users()
                usertable = DataTable(table=users)
                content.add_widget(usertable)

    def update_products(self, code, name, model, qty, purchase, sell, l_sale, before, after, gen, company):

        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Code Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_code = self.products.find_one({'Product_Code' : code})
            if target_code == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Code[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                if name == '':
                    name = target_code["Product_Description"]
                if model == '':
                    model = target_code["Model"]
                if qty == '':
                    qty = target_code["QTY"]
                if purchase == '':
                    purchase = target_code["Purchase_Price"]
                if sell == '':
                    sell = target_code["Sale_Price"]
                if l_sale == '':
                    l_sale = target_code["Last_Sale"]
                if before == '':
                    before = target_code["Before"]
                if after == '':
                    after = target_code["After"]
                if gen == '':
                    name = target_code["Gen"]
                if company == '':
                    name = target_code["Company"]


            self.products.update_one({'Product_Code': code}, {
                '$set': {"Product_Code": code, "Product_Description": name, "Model": model, "QTY": qty,
                         "Purchase_Price": purchase,
                         "Sale_Price": sell, "Last_Sale": l_sale, "Before": before, "After": after, "Gen": gen,
                         "Company": company}})

            content = self.ids.scrn_product_contents
            content.clear_widgets()

            prod = self.get_products()
            prod_table = DataTable(table=prod)
            content.add_widget(prod_table)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='Username')
        crud_submit = Button(text="Remove", size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_users(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_submit = Button(text="Remove", size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_products(crud_code.text))

        target.add_widget(crud_code)
        target.add_widget(crud_submit)

    def remove_users(self, user):
        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]User Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_user = self.users.find_one({'User_Name' : user})
            if target_user == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Users[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                self.users.delete_one({'User_Name': user})
                content = self.ids.scrn_contents
                content.clear_widgets()
                user = self.get_users()
                user_table = DataTable(table=user)
                content.add_widget(user_table)

    def remove_products(self, code):


        if code == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Product Required[/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.kill_switch, 1)
        else:
            target_product = self.users.find_one({'Product_Code ' : code})
            if target_product == None:
                self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Product[/b][/color]', markup=True))
                self.notify.open()
                Clock.schedule_once(self.kill_switch, 1)
            else:
                self.users.delete_one({'Product_Code': code})
                content = self.ids.scrn_product_contents
                content.clear_widgets()
                product = self.get_products()
                prod_table = DataTable(table=product)
                content.add_widget(prod_table)
    def get_users(self):
        client = MongoClient()
        db = client.Test
        users = db.users

        _users = OrderedDict(
            first_names={},
            last_names={},
            user_names={},
            passwords={},
            designations={}

        )
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        designation = []

        for user in users.find():
            first_names.append(user['First_Name'])
            last_names.append(user['Last_Name'])
            user_names.append(user['User_Name'])
            passwords.append(user['Password'])
            designation.append(user['Designation'])

        # /print(first_names)
        user_length = len(first_names)
        idx = 0
        while idx < user_length:
            _users['first_names'][idx] = first_names[idx]
            _users["last_names"][idx] = last_names[idx]
            _users["user_names"][idx] = user_names[idx]
            _users["passwords"][idx] = passwords[idx]
            _users["designations"][idx] = designation[idx]
            idx += 1

        return _users

    def get_products(self):
        client = MongoClient()
        db = client.Test
        products = db.Products
        _product = OrderedDict()
        _product['product_code'] = {}
        _product['product_description'] = {}
        _product['model'] = {}
        _product['qty'] = {}
        _product['purchase_price'] = {}
        _product['sell_price'] = {}
        _product['last_sale'] = {}
        _product['before'] = {}
        _product['after'] = {}
        _product['gen'] = {}
        _product['company'] = {}

        product_code = []
        product_description = []
        model = []
        qty = []
        purchase_price = []
        sell_price = []
        last_sale = []
        before = []
        after = []
        gen = []
        company = []

        for product in products.find():
            product_code.append(product['Product_Code'])
            prod_des = product['Product_Description']
            if len(prod_des) > 13:
                prod_des = prod_des[:13] + '....'
            product_description.append(prod_des)
            model.append(product['Model'])
            qty.append(product['QTY'])
            purchase_price.append(product['Purchase_Price'])
            sell_price.append(product['Sale_Price'])
            try:
                last_sale.append(product['Last_Sale'])
            except KeyError:
                last_sale.append('')
            try:
                before.append(product['Before'])
            except KeyError:
                before.append('0')
            after.append(product['After'])
            gen.append(product['Gen'])
            company.append(product['Company'])

        product_len = len(product_code)
        idx = 0
        while idx < product_len:
            _product['product_code'][idx] = product_code[idx]
            _product['product_description'][idx] = product_description[idx]
            _product['model'][idx] = model[idx]
            _product['qty'][idx] = qty[idx]
            _product['purchase_price'][idx] = purchase_price[idx]
            _product['sell_price'][idx] = sell_price[idx]
            _product['last_sale'][idx] = last_sale[idx]
            _product['before'][idx] = before[idx]
            _product['after'][idx] = after[idx]
            _product['gen'][idx] = gen[idx]
            _product['company'][idx] = company[idx]
            idx += 1
        return _product

    def change_screen(self, instance):
        if instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        elif instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__ == '__main__':
    ad = AdminApp()
    ad.run()
