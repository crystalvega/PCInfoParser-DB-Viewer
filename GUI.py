from tkinter import *
from tkinter import ttk, tix
from textwrap import wrap

import MySQL

second_table = True
global tooltip_window
tooltip_window = None

def Start(Parsinginfo):
    global last
    last = ""
    
    Parsinginfo.append('')
    window = Tk()
    window.title("PCInfoToExcel DB Viewer")  
    
    btn_text = StringVar(value="Общие характеристики")

    window.geometry("800x600")

    def callback1(*arg):
        tree1.delete(*tree1.get_children())
        global last
        if str(combobox1.current()) != last:
            combobox2.set('')
            last = str(combobox1.current())
        if str(var1.get()) != "":
            combobox2['values'] = MySQL.ParseTime(str(var1.get()))
            combobox2['state'] = 'readonly'
        else:
            combobox2['state'] = 'disabled'
            but['state'] = 'disabled'
            for heading in columns_heading1:
                tree1.heading(heading[0], text=heading[1])
        
    def callback2(*arg):
        tree1.delete(*tree1.get_children())
        global second_table
        if str(var2.get()) != "":
            but['state'] = 'normal'
            global strings1
            global strings2
            strings1 = MySQL.ParseTables(str(var1.get()), str(var2.get()),'all configuration')
            strings2 = MySQL.ParseTables(str(var1.get()), str(var2.get()),'disk configuration')
            if second_table:
                for heading in columns_heading2:
                    tree1.heading(heading[0], text=heading[1])
                for strs in strings1: 
                    tree1.insert("", END, values=strs)
            else:
                for heading in columns_heading3:
                    tree1.heading(heading[0], text=heading[1])
                for strs in strings2: 
                    tree1.insert("", END, values=strs)
        else:
            but['state'] = 'disabled'
                
    def callback3(*arg):
        global second_table
        if str(var2.get()) != "":
            global strings1
            global strings2
            tree1.delete(*tree1.get_children())
            second_table = not second_table
            if second_table:
                for heading in columns_heading2:
                    tree1.heading(heading[0], text=heading[1])
                tree1.delete(*tree1.get_children())
                for strs in strings1: 
                    tree1.insert("", END, values=strs)
                btn_text.set("Общие характеристики")
            else:
                for heading in columns_heading3:
                    tree1.heading(heading[0], text=heading[1])
                tree1.delete(*tree1.get_children())
                for strs in strings2: 
                    tree1.insert("", END, values=strs)
                btn_text.set("S.M.A.R.T")

    var1 = StringVar()
    var2 = StringVar()
    
    combobox1 = ttk.Combobox(window, textvariable = var1, font='roboto 14', foreground='#0F0')
    combobox1['values'] = Parsinginfo
    combobox1['state'] = 'readonly'
    combobox1.pack(fill='x',padx= 5, pady=5)
    
    combobox2 = ttk.Combobox(window, textvariable = var2, font='roboto 10', foreground='#0F0')
    combobox2['values'] = ['']
    combobox2['state'] = 'disabled'
    combobox2.pack(fill='x',padx= 5, pady=5)
    
    var1.trace('w', callback1)
    var2.trace('w', callback2)
    
    but = Button(textvariable=btn_text, command=callback3, font='roboto 10')
    but.pack(fill=X)
    but['state'] = 'disabled'
    
    main_frame = Frame(window)
    main_frame.pack(fill=BOTH,expand=1)

    sec = Frame(main_frame)
    sec.pack(fill=X,side=BOTTOM)

    thr = Frame(main_frame)
    thr.pack(fill=Y,side=RIGHT)
    
    columns1 = []
    column_names1 = []
    column_names2 = ['Кабинет', 'LAN', 'ФИО', 'Монитор', 'Диагональ', 'Тип принтера', 'Модель принтера', 'ПК', 'Материнская плата', 'Процессор', 'Частота процессора', 'Баллы Passmark', 'Дата выпуска', 'Тип ОЗУ', 'ОЗУ, 1 Планка', 'ОЗУ, 2 Планка', 'ОЗУ, 3 Планка', 'ОЗУ, 4 Планка', 'Сокет', 'Диск 1', 'Состояние диска 1', 'Диск 2', 'Состояние диска 2', 'Диск 3', 'Состояние диска 3', 'Диск 4', 'Состояние диска 4', 'Операционная система', 'Антивирус', 'CPU Под замену', 'Все CPU под сокет', 'Дата создания']
    column_names3 = ['Кабинет', 'LAN', 'ФИО', 'Диск', 'Наименование', 'Прошивка', 'Размер', 'Время работы', 'Включён', 'Состояние', 'Температура', 'Дата создания']
    
    columns_heading1 = []
    columns_heading2 = []
    columns_heading3 = []
    
    for i in range(0,32):
        if i >= len(column_names1):
            column_names1.append('')
        if i >= len(column_names2):
            column_names2.append('')
        if i >= len(column_names3):
            column_names3.append('')
    for index, column in enumerate(column_names1):
        columns1.append(index)
        columns_heading1.append([index, column])
        columns_heading2.append([index, column_names2[index]])
        columns_heading3.append([index, column_names3[index]])

    
    tree1 = ttk.Treeview(main_frame, columns=columns1, show="headings")
    tree1.pack(side='right',fill=BOTH, expand=1)
    
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("roboto", 9))
    style.configure("Treeview", rowheight=30, font=("roboto", 8))
    for column in tree1["columns"]:
        tree1.column(column, anchor=CENTER)
        tree1.heading(column, text=column)
    
    for heading in columns_heading1:
        tree1.heading(heading[0], text=heading[1])
    

    my_canvas = Canvas(main_frame)
    my_canvas.pack(side=RIGHT,fill=BOTH,expand=1)

    x_scrollbar = ttk.Scrollbar(sec,orient=HORIZONTAL,command=tree1.xview)
    x_scrollbar.pack(side=BOTTOM,fill=X)
    y_scrollbar = ttk.Scrollbar(thr,orient=VERTICAL,command=tree1.yview)
    y_scrollbar.pack(side=LEFT,fill=Y)

    tree1.configure(xscrollcommand=x_scrollbar.set)
    tree1.configure(yscrollcommand=y_scrollbar.set)
    tree1.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL)))  
    tree1.tag_configure('oddrow', background="white")
    tree1.tag_configure('evenrow', background="lightblue")

    def disableEvent(event):
        return "break"
    
    def gen(text):
        text = '\n'.join(wrap(text, width=40))
        global tooltip_window
        tooltip_window = Toplevel(window)
        tooltip_label = Label(tooltip_window, 
                                text=text)
        tooltip_label.pack()
    
        tooltip_window.overrideredirect(True)
    
        x = window.winfo_pointerx() + 20
        y = window.winfo_pointery() + 20
        tooltip_window.geometry("+{}+{}".format(x, y))
        
    def destroy():
        global tooltip_window
        tooltip_window.destroy()
        tooltip_window = None
    
    def textEvent(event):
        x, y = event.x, event.y
        try:
            destroy()
        except Exception:
            Exception
        iid = tree1.identify_row(y)
        xid = tree1.identify_column(x)
        if iid:
            try:
                item = tree1.item(iid)['values'][int(xid.replace('#',''))-1].rstrip()
                if len(item) > 35:
                    gen(item)
            except IndexError:
                Exception
            
        
    tree1.bind("<Button-1>", disableEvent)
    tree1.bind("<Motion>", textEvent)
    global last_focus
    last_focus = None

    window.mainloop()

def DisplayInfo():
    print(4)