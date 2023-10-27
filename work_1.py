# Импортировать библиотеку 'tkinter':
import tkinter as tk
# Импортировать из библиотеки 'tkinter' модуль, отвечающий за объекты класса 'Treeview':
from tkinter import ttk
# Импортировать библиотеку SQLite3:
import sqlite3

#=== Класс Main(tk.Frame) =========================================================================

# Создать класс приложения:
class Main(tk.Frame):
    # Определить и реализовать метод инициализации приложения:
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()	    # вызывать данный метод при каждой инициализации главного окна приложения

    # Определить и реализовать метод поиска всех выделенных строк из таблицы 'db':
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', name) 
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # Определить и реализовать метод открытия дочернего окна поиска данных в таблице БД:
    def open_search_dialog(self):
        Search()

    # Определить и реализовать метод удаления всех выделенных строк из таблицы 'db':
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE ID=?', 
            (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Определить и реализовать метод редактирования объектов класса БД:
    def update_record(self, name, tel, email):
        self.db.cur.execute('UPDATE db SET name=?, tel=?, email=? WHERE ID=?', 
            (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()
    # Здесь self.tree.selection() возвращает все выделенные строки таблицы 'db'.
    # [0] - означает выбор 1-й выделенной строки (строки под индексом 0);
    # '#1' - означает выбор значения из 1-го столбца (т.е. столбца 'id') этой строки.

    # Определить и реализовать метод редактирования данных в таблице БД:
    def open_update_dialog(self):
        Update()

    # Определить и реализовать метод отображения данных из таблицы БД в главном окне приложения:
    def view_records(self):
        # Выбрать все данные из таблицы БД в результирующее множество:
        self.db.cur.execute('SELECT * FROM db;')
        # Стереть из виджета Treeview всю предыдущую информацию:
        [self.tree.delete(i) for i in self.tree.get_children()]
        # Добавить в виджет Treeview все данные из результирующего множества:
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]
    
    # Определить и реализовать метод добавления новых данных в Телефонную книгу:
    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    # Определить и реализовать метод создания и открытия вторичного окна:
    def open_dialog(self):
        Child()

    # Определить и реализовать метод создания всех виджетов главного окна приложения:
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Создать в Панели инструментов (Toolbar) кнопку добавления записи:
        self.add_img = tk.PhotoImage(file='./img/add.png')
        # command - функция, выполняемая при нажатии на кнопку
        # bg - фон
        # bd - граница
        # image - пиктограмма кнопки
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        # упаковать и выровнять виджет кнопки по левому краю:
        btn_open_dialog.pack(side=tk.LEFT)

        # Добавить объект класса Treeview
        # columns - столбцы
        # height - высота таблицы
        # show='headings' - скрыть нулевую (пустую) колонку таблицы
        self.tree = ttk.Treeview(self,columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')

        # добавить параметры колонкам:
        # width - ширину
        # anchor - выравнивание текста в ячейке
        self.tree.column("ID", width=30, anchor=tk.W)
        self.tree.column("name", width=250, anchor=tk.W)
        self.tree.column("tel", width=150, anchor=tk.W)
        self.tree.column("email", width=250, anchor=tk.W)

        # добавить заглавия колонкам:
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')

        # упаковать:
        self.tree.pack(side=tk.LEFT)

        # Создать в Панели инструментов (Toolbar) кнопку изменения записи:
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, 
                                    command=self.open_update_dialog)
        # упаковать и выровнять виджет кнопки по левому краю:
        btn_edit_dialog.pack(side=tk.LEFT)

        # Создать в Панели инструментов (Toolbar) кнопку удаления записи:
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                     image=self.delete_img, command=self.delete_records)
        # упаковать и выровнять виджет кнопки по левому краю:
        btn_delete.pack(side=tk.LEFT)

        # Создать в Панели инструментов (Toolbar) кнопку поиска записи:
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                     image=self.search_img, command=self.open_search_dialog)
        # упаковать и выровнять виджет кнопки по левому краю:
        btn_search.pack(side=tk.LEFT)

        # Создать в Панели инструментов (Toolbar) кнопку "Обновить" [виджет Treeview]:
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                     image=self.refresh_img, command=self.view_records)
        # упаковать и выровнять виджет кнопки по левому краю:
        btn_refresh.pack(side=tk.LEFT)

#=== Класс Child(tk.Toplevel) =====================================================================

# Создать класс дочерних (или вторичных) окон:
class Child(tk.Toplevel):
    # Определить и реализовать метод инициализации вторичного окна:
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Определить и реализовать метод отрисовки вторичного окна:
    def init_child(self):
        self.title('Добавить')          # задать заголовок вторичного окна
        self.geometry('400x200')        # задать геометрию вторичного окна
        self.resizable(False, False)    # зафиксировать размер вторичного окна
        self.grab_set()                 # блокировать главное окно приложения при открытом вторичном окне
        self.focus_set()                # сделать активным вторичное окно

        # Создать и настроить надписи во вторичном окне:
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)

        # Добавить строку ввода для ФИО:
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=120, y=50, width=250)

        # Добавить строку ввода для Телефона:
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=120, y=80, width=250)

        # Добавить строку ввода для email:
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=120, y=110, width=250)

        # Создать в дочернем окне кнопку [Закрыть]:
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Создать в дочернем окне кнопку [Добавить]:
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        # Настроить срабатывание кнопки [Добавить] по ЛКМ:
        self.btn_ok.bind('<Button-1>', lambda event:
            self.view.records(self.entry_name.get(),
                              self.entry_tel.get(),
                              self.entry_email.get()))

#=== Класс Update(Child) ==========================================================================

class Update(Child):
    # Определить и реализовать метод инициализации объектов класса Update:
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Определить и реализовать метод отрисовки дочернего окна для редактирования записи в таблице БД:
    def init_edit(self):
        self.title("Редактировать позицию")  # задать заголовок данного дочернего окна
        # Создать кнопку "Редактировать":
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=185, y=170)
        # Настроить реакцию кнопки "Редактировать" на её нажатие:
        btn_edit.bind('<Button-1>', lambda event:
            self.view.update_record(self.entry_name.get(),
                                    self.entry_tel.get(),
                                    self.entry_email.get()))
        # После чего следует ещё и автоматически закрыть дочернее окно редактирования.
        # Предложение "add='+'" позволяет на одну кнопку навесить более одного события:
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    # Определить и реализовать метод заполнения формы дочернего окна редактирования данными из выбранной таблицы БД:
    def default_data(self):
        self.db.cur.execute('SELECT * FROM db WHERE ID=?', 
            (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # Получить доступ к 1-й записи из выборки:
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])

#=== Класс Search(tk.Toplevel) ====================================================================

class Search(tk.Toplevel):  # класс Search наследует от класса Toplevel
    # Определить и реализовать метод инициализации объектов класса Search:
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Определить и реализовать метод отрисовки дочернего окна для редактирования записи в таблице БД:
    def init_search(self):
        self.title("Поиск")  # задать заголовок данного дочернего окна
        self.geometry('400x120')
        self.resizable(False, False)
        # Создать надпись-заглавие для поля ввода:
        label_search = tk.Label(self, text="Поиск")
        label_search.place(x=30, y=40)
        # Создать поле для ввода:
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=40, width=250)
        # Создать кнопку закрытия окна:
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=260, y=90)
        # Создать кнопку "Поиск":
        btn_search = ttk.Button(self, text="Поиск")
        btn_search.place(x=180, y=90)
        # Настроить реакцию кнопки "Поиск" на её нажатие:
        btn_search.bind('<Button-1>', lambda event:
            self.view.search_records(self.entry_search.get()))
        # После этого следует автоматически закрывать дочернее окно редактирования.
        # Предложение "add='+'" позволяет на одну кнопку навесить более одного события:        
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

#=== Класс DB =====================================================================================

# Создать класс БД:
class DB:
    # Определить и реализовать метод инициализации объектов класса БД:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS db(
            ID INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT);
        ''')
        self.conn.commit()

    # Определить и реализовать метод заполнения объектов класса БД:
    def insert_data(self, name, tel, email):
        self.cur.execute('''INSERT INTO db(name, tel, email)
        VALUES (?, ?, ?);
        ''', (name, tel, email))    
        self.conn.commit()

#=== Работа с приложением =========================================================================

# Проверить, в каком месте запускается приложение:
if __name__ == '__main__':  # если приложение запускается на локальном ПК (а, к примеру, не в облаке), тогда:
    root = tk.Tk()      # создать в переменной 'root' объект класса главного окна приложения
    db = DB()           # создать в переменной 'db' объект класса БД
    app = Main(root)    # создать в переменной 'app' объект класса приложения
    app.pack()          # отрисовать главное окно данного приложения
    root.title('Телефонная книга')  # присвоить заголовок главному окну приложения
    root.geometry('800x600')        # задать геометрию главного окна приложения
    root.resizable(False, False)    # зафиксировать размер главного окна приложения
    root.mainloop()     # ввести приложение в его главный условно бесконечный цикл ожидания любых событий
