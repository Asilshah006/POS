import re

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from pymongo import MongoClient
from datetime import datetime
from kivy.lang import Builder

# Builder.load_file('operator_pack/Operator.kv')

class OperatorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        client = MongoClient()
        self.db = client.Test
        self.products = self.db.Products
        self.users = self.db.users

        self.cart = []
        self.qty = []
        self.total = 0.00

    def logout_op(self):
        self.parent.parent.current = 'scrn_si'

    def update_purchases(self):

        pcode = self.ids.code_input.text
        pcode = pcode.upper()
        product_container = self.ids.Products

        target_code = self.products.find_one({'Product_Code' : pcode})
        if target_code == None:
            pass
        else:
            details = BoxLayout(size_hint_y=None , height=30, pos_hint={'top': 1})

            product_container.add_widget(details)

            qty_input = self.ids.qty_input.text



            if qty_input == '':
                qty_input = '1'


            code = Label(text=pcode, size_hint_x = 0.1, color = (0,0,0.45,1))
            name = Label(text=target_code['Product_Description'], size_hint_x = 0.3, color = (0,0,0.45,1))
            model = Label(text= target_code['Model'], size_hint_x = 0.1, color = (0,0,.45,1) )
            disc = Label(text='0.00', size_hint_x = 0.1, color = (0,0,0.45,1))
            qty = Label(text=qty_input, size_hint_x = 0.1, color = (0,0,0.45,1))
            price= Label(text=target_code['Sale_Price'], size_hint_x = 0.1, color = (0,0,0.45,1))

            total_price = int(qty_input) * float(target_code['Sale_Price'])
            total = Label(text=str(total_price), size_hint_x=0.1,
                          color=(0, 0, 0.45, 1))

            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(model)
            details.add_widget(disc)
            details.add_widget(qty)
            details.add_widget(price)

            pname = name.text
            pprice = float(price.text)

            pmodel = model.text
            self.total += total_price
            self.ids.cur_product.text = pname
            self.ids.cur_price.text = str(pprice)
            purchaseTotal = '`\n\nTotal\t\t\t\t\t\t\t\t'+ str(self.total)
            preview = self.ids.recipt_preview
            prev_text = preview.text
            __date = prev_text.find('Date:')
            if __date > 0:
                prev_text = prev_text + str(datetime.now())
            __prev = prev_text.find('`')
            if __prev > 0:
                prev_text = prev_text[:__prev]

            ptarget = -1
            for i , c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i

            if ptarget>=0:
                qty_input= int(self.qty[ptarget]) + int(qty_input)
                self.qty[ptarget] = int(qty_input)
                pqty = qty_input
                print(pqty)
                expr = '%s\t\tx\d\t'%(pmodel)
                reexpr = pmodel+'\t\tx'+str(qty_input)+'\t'
                nu_expr = re.sub(expr, reexpr, prev_text)
                preview.text = nu_expr + purchaseTotal
            else:
                self.cart.append(pcode)
                self.qty.append(qty_input)
                nu_preview = '\n\n'.join([prev_text,pname+'\t\t'+ pmodel +'\t\tx'+ str(qty_input) + '\t\t' + str(pprice), purchaseTotal])
                preview.text = nu_preview
        self.ids.disc_input.text = '0.00'
        self.ids.disc_perc_input.text = '0'
        self.ids.after_input.text = str(int(target_code['Before']) -1)
        self.ids.price_input.text = str(pprice)
        self.ids.total_input.text = str(pprice)


        details.add_widget(total)

class OperatorApp(App):
    def build(self):
        return OperatorWindow()



if __name__ == '__main__':
    oa = OperatorApp()
    oa.run()
