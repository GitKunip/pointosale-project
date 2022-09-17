import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import *
import datetime
import quickstart as qs
import math

qt_creator_file = "lamozaposui.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_creator_file)


class Menu:
    def __init__(self):
        self.items = []
        self.options = {}
        self.prices = {}
        self.discounts = {}

    def get_item_index(self, item):
        for index, it in enumerate(self.items):
            if it == item:
                return index

    def priced(self, item, quantity, additional=''):
        if additional:
            return self.prices[item][additional] * quantity
        else:
            return self.prices[item] * quantity

    def discounted(self, item, quantity):
        if self.discounts[item]:
            return self.discounts[item] * self.prices[item] * quantity
        else:
            return 0


class TodoModel(QtCore.QAbstractListModel):
    def __init__(self, *args, todos=None, **kwargs):
        super(TodoModel, self).__init__(*args, **kwargs)
        self.todos = todos or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            item, _, _, _ = self.todos[index.row()]
            return item

    def rowCount(self, index):
        return len(self.todos)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("D'La Moza Tamansari")

        # Storing menu items, prices, options, discounts in menu objects for each order type.
        self.grabfood = Menu()
        self.shopeefood = Menu()
        self.gofood = Menu()
        self.direct = Menu()

        # Fetching items, prices, and options data from google sheets and setting up the list in combo box.
        for menu, text, comb in [(self.grabfood, 'GRABFOOD', self.menuGrabfood),
                                 (self.shopeefood, 'SHOPEEFOOD', self.menuShopeefood),
                                 (self.gofood, 'GOFOOD', self.menuGofood),
                                 (self.direct, 'DIRECT', self.menuDirect)]:
            qs.fetch_menu_data(menu, text, comb)
            self.topping_choice(menu, comb.currentText())

        # Create daily first entry of balance information:
        now = datetime.datetime.now()
        date = f"{now.day}/{now.month}/{now.year}"
        qs.daily_balance_check(date)

        # State components:
        self.items = TodoModel()
        self.itemsView.setModel(self.items)
        self.qty = 0
        self.quant.setText(str(self.qty))
        self.details = ''
        self.detailsLabel.setText(self.details)
        self.update_items = []
        self.expenseProperty = False
        self.expenseAmount = ''
        # Hooking up the application logic:
        self.orderType.currentIndexChanged.connect(lambda: self.index_adjust(self.orderType.currentIndex()))

        # # Below are the implemented 'unordered list/ dictionary' to display the preferred topping options based on
        # # menuObject.options['menu item text']. Refer to topping_choice function for clarity:
        self.menuGrabfood.currentIndexChanged.connect(lambda: self.topping_choice(self.grabfood,
                                                                                  self.menuGrabfood.currentText()))
        self.menuGofood.currentIndexChanged.connect(lambda: self.topping_choice(self.gofood,
                                                                                self.menuGofood.currentText()))
        self.menuShopeefood.currentIndexChanged.connect(lambda: self.topping_choice(self.shopeefood,
                                                                                    self.menuShopeefood.currentText()))
        self.menuDirect.currentIndexChanged.connect(lambda: self.topping_choice(self.direct,
                                                                                self.menuDirect.currentText()))
        # # Refresh menu feature below
        self.updateMenu.clicked.connect(lambda: self.refresh_menu())
        # # Refresh menu feature above

        # # Visual cues indicating the app flow for the user:
        self.visual_cue(state='off')

        # # On-screen number and letter key logic:
        self.minusQty.clicked.connect(lambda: self.quantity_adjust('subtract'))
        self.addQty.clicked.connect(lambda: self.quantity_adjust('add'))

        self.key1.pressed.connect(lambda: self.input_details('1', expense=self.expenseProperty))
        self.key2.pressed.connect(lambda: self.input_details('2', expense=self.expenseProperty))
        self.key3.pressed.connect(lambda: self.input_details('3', expense=self.expenseProperty))
        self.key4.pressed.connect(lambda: self.input_details('4', expense=self.expenseProperty))
        self.key5.pressed.connect(lambda: self.input_details('5', expense=self.expenseProperty))
        self.key6.pressed.connect(lambda: self.input_details('6', expense=self.expenseProperty))
        self.key7.pressed.connect(lambda: self.input_details('7', expense=self.expenseProperty))
        self.key8.pressed.connect(lambda: self.input_details('8', expense=self.expenseProperty))
        self.key9.pressed.connect(lambda: self.input_details('9', expense=self.expenseProperty))
        self.key0.pressed.connect(lambda: self.input_details('0', expense=self.expenseProperty))
        self.keyCl.pressed.connect(lambda: self.input_details('CL', expense=self.expenseProperty))
        self.letKey.pressed.connect(lambda: self.inputKey.setCurrentIndex(1))

        self.keyq.pressed.connect(lambda: self.input_details('Q'))
        self.keyw.pressed.connect(lambda: self.input_details('W'))
        self.keye.pressed.connect(lambda: self.input_details('E'))
        self.keyr.pressed.connect(lambda: self.input_details('R'))
        self.keyt.pressed.connect(lambda: self.input_details('T'))
        self.keyy.pressed.connect(lambda: self.input_details('Y'))
        self.keyu.pressed.connect(lambda: self.input_details('U'))
        self.keyi.pressed.connect(lambda: self.input_details('I'))
        self.keyo.pressed.connect(lambda: self.input_details('O'))
        self.keyp.pressed.connect(lambda: self.input_details('P'))
        self.keya.pressed.connect(lambda: self.input_details('A'))
        self.keys.pressed.connect(lambda: self.input_details('S'))
        self.keyd.pressed.connect(lambda: self.input_details('D'))
        self.keyf.pressed.connect(lambda: self.input_details('F'))
        self.keyg.pressed.connect(lambda: self.input_details('G'))
        self.keyh.pressed.connect(lambda: self.input_details('H'))
        self.keyj.pressed.connect(lambda: self.input_details('J'))
        self.keyk.pressed.connect(lambda: self.input_details('K'))
        self.keyl.pressed.connect(lambda: self.input_details('L'))
        self.keyz.pressed.connect(lambda: self.input_details('Z'))
        self.keyx.pressed.connect(lambda: self.input_details('X'))
        self.keyc.pressed.connect(lambda: self.input_details('C'))
        self.keyv.pressed.connect(lambda: self.input_details('V'))
        self.keyb.pressed.connect(lambda: self.input_details('B'))
        self.keyn.pressed.connect(lambda: self.input_details('N'))
        self.keym.pressed.connect(lambda: self.input_details('M'))
        self.spaceKey.pressed.connect(lambda: self.input_details(' '))
        self.numKey.pressed.connect(lambda: self.inputKey.setCurrentIndex(0))
        self.delKey.pressed.connect(lambda: self.input_details('<<<'))
        # # Menu-ordering logic:
        self.addItem.pressed.connect(self.add_item)
        self.deleteItem.pressed.connect(self.delete_item)
        self.placeOrder.pressed.connect(self.place_order)
        # # Updating expense:
        self.updateExpenses.pressed.connect(self.update_expenses)

    def index_adjust(self, n):
        """Adjusting the type of menu and topping option to be displayed
         by evaluating the current index (n) of orderType (QComboBox element).
         Adjustment is made by changing the current index of menuItem and ToppingChoice, both of which are
         QStackedWidget elements. This function also resets the state to its default."""

        # Setting the states to default:
        self.reset_data()

        # Visual cue indicating the app flow for the user:
        self.visual_cue(state='off')

        # Menu adjustment:
        self.menuItem.setCurrentIndex(n)

        # Order Details adjustment
        self.DetailsCode.setCurrentIndex(n)
        if self.DetailsCode.currentIndex() == 3:
            self.inputKey.setCurrentIndex(1)
            # Enabling payment option
            self.frame_6.setGeometry(20, 300, 591, 451)  # Increase frame_6 (order summary frame) Y pos by 70, 230+70
            # = 300
            self.detailsLabel.setGeometry(180, 170, 391, 51)  # Increase 'Order Details'-box width by 30, 361 + 30 = 391
            self.deleteItem.setGeometry(20, 770, 281, 75)
            self.placeOrder.setGeometry(330, 770, 281, 75)
        else:
            self.inputKey.setCurrentIndex(0)
            # Disabling payment option
            self.frame_6.setGeometry(20, 230, 591, 451)  # Default position of frame_6
            self.detailsLabel.setGeometry(220, 170, 351, 51)  # Default position of 'Order Details'-box
            self.deleteItem.setGeometry(20, 700, 281, 75)
            self.placeOrder.setGeometry(330, 700, 281, 75)

        # Expenses triggered
        if n == 4:
            self.expenseProperty = True
            self.inputKey.setCurrentIndex(0)
            self.DetailsCode.setCurrentIndex(0)
            self.expensesWidget.setGeometry(20, 160, 591, 607)
            self.frame_6.setGeometry(20, 1200, 591, 451)  # Default position of frame_6
            self.frame_2.setGeometry(20, 1200, 591, 71)
            self.detailsLabel.setGeometry(220, 1200, 351, 51)  # Default position of 'Order Details'-box
            self.deleteItem.setGeometry(20, 1200, 281, 75)
            self.placeOrder.setGeometry(330, 1200, 281, 75)
        else:
            self.expenseProperty = False
            self.expensesWidget.setGeometry(20, 1200, 591, 607)
            self.frame_2.setGeometry(20, 160, 591, 71)

        # Topping option adjustment:
        menuName = self.menuItem.currentIndex()
        if menuName == 0:
            self.topping_choice(self.gofood, self.menuGofood.currentText())
        elif menuName == 1:
            self.topping_choice(self.grabfood, self.menuGrabfood.currentText())
        elif menuName == 2:
            self.topping_choice(self.shopeefood, self.menuShopeefood.currentText())
        elif menuName == 3:
            self.topping_choice(self.direct, self.menuDirect.currentText())

    def visual_cue(self, state=''):
        if state.lower() == 'on':
            for frame in [self.frame_3, self.frame_4, self.frame_5, self.frame_7, self.frame_8, self.frame_9,
                          self.frame_10, self.frame_12, self.frame_13, self.frame_14, self.frame_15, self.frame_16,
                          self.placeOrder]:
                frame.setEnabled(True)
        else:
            for frame in [self.frame_3, self.frame_4, self.frame_5, self.frame_7, self.frame_8, self.frame_9,
                          self.frame_10, self.frame_12, self.frame_13, self.frame_14, self.frame_15, self.frame_16,
                          self.placeOrder, self.addItem]:
                frame.setEnabled(False)

    def refresh_menu(self):
        menuName = self.menuItem.currentIndex()
        if menuName == 0:
            qs.fetch_menu_data(self.gofood, 'GOFOOD', self.menuGofood, refresh=1)
        elif menuName == 1:
            qs.fetch_menu_data(self.grabfood, 'GRABFOOD', self.menuGrabfood, refresh=1)
        elif menuName == 2:
            qs.fetch_menu_data(self.shopeefood, 'SHOPEEFOOD', self.menuShopeefood, refresh=1)
        elif menuName == 3:
            qs.fetch_menu_data(self.direct, 'DIRECT', self.menuDirect, refresh=1)

    def topping_choice(self, menuObject, text):
        try:
            self.qty = 0
            self.quant.setText('0')
            choice = menuObject.options[text]
            self.ToppingChoice.setCurrentIndex(choice)
        except KeyError:
            pass

    def quantity_adjust(self, param):
        if param == 'add':
            self.qty += 1
            self.quant.setText(str(self.qty))
            if self.qty > 0:
                self.minusQty.setEnabled(True)
                self.addItem.setEnabled(True)
        elif param == 'subtract':
            self.qty -= 1
            self.quant.setText(str(self.qty))
            if self.qty == 0:
                self.minusQty.setEnabled(False)
                self.addItem.setEnabled(False)

    def input_details(self, key, expense=False):
        # There's a bug which causes mismatch between menu item and topping option at the start of the app.
        # Since its location is unknowable, I chose to correct the mismatch by making use of the user flow:
        # topping adjustment function will be run each time the user types in order details.

        # Topping option adjustment below.
        menuName = self.menuItem.currentIndex()
        if menuName == 0:
            self.topping_choice(self.gofood, self.menuGofood.currentText())
        elif menuName == 1:
            self.topping_choice(self.grabfood, self.menuGrabfood.currentText())
        elif menuName == 2:
            self.topping_choice(self.shopeefood, self.menuShopeefood.currentText())
        elif menuName == 3:
            self.topping_choice(self.direct, self.menuDirect.currentText())
        # Topping adjustment above.

        if expense:
            if key == 'CL':
                self.expenseAmount = ''
            else:
                self.expenseAmount += key
            self.expensed.setText(self.expenseAmount)

            if len(self.expenseAmount) >= 4:
                self.updateExpenses.setEnabled(True)
            else:
                self.updateExpenses.setEnabled(False)
        else:
            if key == 'CL':
                self.details = ''
            elif key == '<<<':
                self.details = self.details[:-1]
            else:
                self.details += key
            self.detailsLabel.setText(self.details)

            if len(self.details) >= 3:
                self.visual_cue(state='on')
            else:
                self.visual_cue(state='off')

    def option_nil(self, menu_item):

        if menu_item.currentText() in ['(L)', '(R)', '(M)']:
            item_string = f'{self.quant.text()} x {self.singleTop.currentText()} {menu_item.currentText()}'
            update_items = [f'{self.singleTop.currentText()} {menu_item.currentText()}', int(self.quant.text())]
            return item_string, update_items
        else:
            item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                           f'\n    Combo Pizza 1'
                           f'\n    {self.singleTop.currentText()}')
            update_items = [f'{menu_item.currentText()}\n    Combo Pizza 1: {self.singleTop.currentText()}',
                            int(self.quant.text())]
            return item_string, update_items

    def option_one(self, menu_item):

        item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                       f'\n    Combo Pizza 1'
                       f'\n    {self.doubleTopA.currentText()}'
                       f'\n    Combo Pizza 2'
                       f'\n    {self.doubleTopB.currentText()}')
        update_items = [f'{menu_item.currentText()}\n    Combo Pizza 1: {self.doubleTopA.currentText()}'
                        f'\n    Combo Pizza 2: {self.doubleTopB.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_two(self, menu_item):

        item_string = f'{self.quant.text()} x {menu_item.currentText()} \n    {self.extraTop.currentText()}'
        update_items = [f'{menu_item.currentText()} : {self.extraTop.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_three(self, menu_item):

        item_string = f'{self.quant.text()} x {menu_item.currentText()}'
        update_items = [f'{menu_item.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_four(self, menu_item):

        item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                       f'\n    Combo Pizza 1'
                       f'\n    {self.TripleTopA.currentText()}'
                       f'\n    Combo Pizza 2'
                       f'\n    {self.TripleTopB.currentText()}'
                       f'\n    Combo Pizza 3'
                       f'\n    {self.TripleTopC.currentText()}')
        update_items = [f'{menu_item.currentText()}\n    Combo Pizza 1: {self.TripleTopA.currentText()}'
                        f'\n    Combo Pizza 2: {self.TripleTopB.currentText()}'
                        f'\n    Combo Pizza 3: {self.TripleTopC.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_five(self, menu_item):

        item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                       f'\n    Combo Pizza 1'
                       f'\n    {self.toppingComboPan.currentText()}'
                       f'\n    Combo Drink'
                       f'\n    {self.toppingComboDrink.currentText()}')
        update_items = [f'{menu_item.currentText()}\n    Combo Pizza 1: {self.toppingComboPan.currentText()}'
                        f'\n    Combo Drink: {self.toppingComboDrink.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_six(self, menu_item):

        item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                       f'\n    {self.addDrink.currentText()}')
        update_items = [f'{menu_item.currentText()}\n    {self.addDrink.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def option_seven(self, menu_item):

        item_string = (f'{self.quant.text()} x {menu_item.currentText()}'
                       f'\n    Combo Pizza (L)'
                       f'\n    {self.toppingLarge.currentText()}'
                       f'\n    Combo Pizza (M)'
                       f'\n    {self.toppingMedium.currentText()}')
        update_items = [f'{menu_item.currentText()}\n    Combo Pizza (L): {self.toppingLarge.currentText()}'
                        f'\n    Combo Pizza (M): {self.toppingMedium.currentText()}', int(self.quant.text())]
        return item_string, update_items

    def add_item(self):

        item_string = ''
        item_quantity = int(self.quant.text())
        update_array = []
        menu_object = {0: self.gofood, 1: self.grabfood, 2: self.shopeefood, 3: self.direct}
        menu_item = {0: self.menuGofood, 1: self.menuGrabfood, 2: self.menuShopeefood, 3: self.menuDirect}
        menu_object = menu_object.get(self.orderType.currentIndex())
        menu_item = menu_item.get(self.orderType.currentIndex())
        option_index = menu_object.options[menu_item.currentText()]
        item_price = 0
        item_discount = 0

        # An additional condition for fetching items other than Extra Topping and Additional Drinks Package prices
        # because both of them have a dictionary data type as their price value instead of integer.
        if option_index not in [2, 6]:
            item_price = menu_object.priced(menu_item.currentText(), item_quantity)
            item_discount = int(menu_object.discounted(menu_item.currentText(), item_quantity))

        if option_index == 0:
            item_string, update_array = self.option_nil(menu_item)
        elif option_index == 1:
            item_string, update_array = self.option_one(menu_item)
        elif option_index == 2:
            item_price = menu_object.priced(menu_item.currentText(), item_quantity,
                                            additional=self.extraTop.currentText())
            item_discount = int(menu_object.discounted(menu_item.currentText(), item_quantity))
            item_string, update_array = self.option_two(menu_item)
        elif option_index == 3:
            item_string, update_array = self.option_three(menu_item)
        elif option_index == 4:
            item_string, update_array = self.option_four(menu_item)
        elif option_index == 5:
            item_string, update_array = self.option_five(menu_item)
        elif option_index == 6:
            item_price = menu_object.priced(menu_item.currentText(), item_quantity,
                                            additional=self.addDrink.currentText())
            item_discount = int(menu_object.discounted(menu_item.currentText(), item_quantity))
            item_string, update_array = self.option_six(menu_item)
        elif option_index == 7:
            item_string, update_array = self.option_seven(menu_item)
        # print(f'Option {option_index}')
        self.update_items.append(update_array)
        self.items.todos.append((item_string, item_quantity, item_price, item_discount))
        self.items.layoutChanged.emit()
        # There was a bug: type(item_price) doesn't log out int, there by resulting in TypeError in line 363
        # for s, q, p, d in self.items.todos:
        #     print(p, type(p))
        #     print(d, type(d))
        # The print command above is used to detect where the bug might be. You have to try ordering all the menus from
        # each order type. FOUND IT! THE BUG HAPPENS BECAUSE THE PRICES AND DISCOUNTS OF GOFOOD AND SHOPEEFOOD are EMPTY

        # Sets up the UI and the states for the next user loop for adding items
        self.qty = 0
        self.quant.setText(str(self.qty))
        self.minusQty.setEnabled(False)
        self.addItem.setEnabled(False)
        if len(self.items.todos) > 0:
            self.placeOrder.setEnabled(True)
        else:
            self.placeOrder.setEnabled(False)

    def reset_data(self):
        self.qty = 0
        self.quant.setText(str(self.qty))
        self.details = ''
        self.detailsLabel.setText(self.details)
        self.expenseAmount = ''
        self.expensed.setText(self.expenseAmount)
        self.update_items = []
        self.items.todos = []
        self.items.layoutChanged.emit()
        self.itemsView.clearSelection()

    def delete_item(self):
        indexes = self.itemsView.selectedIndexes()
        if indexes:
            index = indexes[0]
            self.update_items.pop(index.row())
            del self.items.todos[index.row()]
            self.items.layoutChanged.emit()
            self.itemsView.clearSelection()
        if len(self.items.todos) > 0:
            self.placeOrder.setEnabled(True)
        else:
            self.placeOrder.setEnabled(False)

    def update_expenses(self):
        admin = self.cashierName.currentText()
        now = datetime.datetime.now()
        date = f"{now.day}/{now.month}/{now.year}"
        time = f"{now.hour}:{now.minute}"
        debit = int(self.expensed.text())
        update_array = [date, time, admin, self.orderType.currentText(), self.expenseType.currentText(), debit]
        qs.expense_update(update_array)
        self.reset_data()
        self.visual_cue(state='off')
        self.orderType.setCurrentIndex(0)

    def place_order(self):
        # Assembling the details into an array (update_array) and then upload it into sales sheet using quickstart
        admin = self.cashierName.currentText()
        now = datetime.datetime.now()
        date = f"{now.day}/{now.month}/{now.year}"
        time = f"{now.hour}:{now.minute}"
        labeling = {'GOFOOD': 'F' + self.detailsLabel.text(),
                    'GRABFOOD': 'GF' + self.detailsLabel.text(),
                    'SHOPEE': '#' + self.detailsLabel.text(),
                    'DIRECT': self.detailsLabel.text()}
        order_label = labeling.get(self.orderType.currentText())
        total_sales = 0
        credit = 0
        payment = ''
        # Calculate total sales
        for _, _, item_price, item_discount in self.items.todos:
            total_sales += item_price
            if item_discount:
                total_sales -= item_discount
        # Rounding down the numbers
        total_sales /= 10
        total_sales = math.floor(total_sales)
        total_sales *= 10

        # Checking for order type
        if self.orderType.currentText() == 'DIRECT':
            payment = self.payOption.currentText()
            if self.payOption.currentText() == 'CASH':
                credit = total_sales

        update_array = [date, time, admin, self.orderType.currentText(), order_label, self.update_items,
                        total_sales, payment, credit]

        # print(update_array)
        qs.sales_update(update_array)

        # Sets up the UI for next user loop
        # self.items.todos = []
        # self.items.layoutChanged.emit()
        # self.itemsView.clearSelection()
        # self.details = ''
        # self.update_items = []
        # self.detailsLabel.setText(self.details)
        self.reset_data()
        self.visual_cue(state='off')
        self.orderType.setCurrentIndex(0)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
