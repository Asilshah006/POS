from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from collections import OrderedDict
from kivy.lang import Builder
from pymongo import MongoClient

Builder.load_string('''
<DataTable>:
    id:main_win
    RecycleView:
        viewclass: 'CustLabel'
        id: table_floor
        RecycleGridLayout:
            id:table_floor_layout
            cols :10
            default_size:(None , 250)
            default_size_hint:(1,None)
            size_hint_y:None
            height: self.minimum_height
            spacing:5             
<CustLabel@Label>:
    bcolor:(1,1,1,1)
    canvas.before:
        Color:
            rgba:root.bcolor
        Rectangle:
            size:self.size
            pos:self.pos
        
  ''')


class DataTable(BoxLayout):
    def __init__(self,table = '', **kwargs):
        super().__init__(**kwargs)

        # products = self.get_products()
        products = table
        col_keys = [k for k in products.keys()]
        row_len = len(products[col_keys[0]])
        print(col_keys)
        print(row_len)
        self.columns = len(col_keys)
        self.ids.table_floor_layout.cols = self.columns
        table_data = []
        for t in col_keys:
            table_data.append({'text' : str(t),'size_hint_y' : None , 'height' : 50, 'bcolor' : (0,0,0.45,1)})
        for r in range(row_len):
            for c in col_keys:
                table_data.append({'text': str(products[c][r]),'size_hint_y' :None , 'height' : 50, 'bcolor' : (0,0,0.45,1)})

        self.ids.table_floor.data = table_data


#     def get_products(self):
#         client = MongoClient()
#         db = client.Test
#         products = db.Products
#         _product = OrderedDict()
#         _product['product_code'] = {}
#         _product['product_description'] = {}
#         _product['model'] = {}
#         _product['qty'] = {}
#         _product['purchase_price'] = {}
#         _product['sell_price'] = {}
#         _product['last_sale'] = {}
#         _product['before'] = {}
#         _product['after'] = {}
#         _product['gen'] = {}
#         _product['company'] = {}
#
#         product_code = []
#         product_description = []
#         model = []
#         qty = []
#         purchase_price = []
#         sell_price = []
#         last_sale = []
#         before = []
#         after = []
#         gen = []
#         company = []
#         for product in products.find():
#             product_code.append(product['Product_Code'])
#             product_description.append(product['Product_Description'])
#             model.append(product['Model'])
#             qty.append(product['QTY'])
#             purchase_price.append(product['Purchase_Price'])
#             sell_price.append(product['Sale_Price'])
#             last_sale.append(product['Last_Sale'])
#             before.append(product['Before'])
#             after.append(product['After'])
#             gen.append(product['Gen'])
#             company.append(product['Company'])
#
#         product_len = len(product_code)
#         idx = 0
#         while idx < product_len:
#             _product['product_code'][idx] = product_code[idx]
#             _product['product_description'][idx] = product_description[idx]
#             _product['model'][idx] = model[idx]
#             _product['qty'][idx] = qty[idx]
#             _product['purchase_price'][idx] = purchase_price[idx]
#             _product['sell_price'][idx] = sell_price[idx]
#             _product['last_sale'][idx] = last_sale[idx]
#             _product['before'][idx] = before[idx]
#             _product['after'][idx] = after[idx]
#             _product['gen'][idx] = gen[idx]
#             _product['company'][idx] = company[idx]
#             idx += 1
#         return _product
#
#
# class DataTableApp(App):
#     def build(self):
#         return DataTable()
#
#
# if __name__ == '__main__':
#     dt = DataTableApp()
#     dt.run()
