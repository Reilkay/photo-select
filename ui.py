import tkinter as tk
from tkinter.filedialog import (askopenfilename, askopenfilenames,
                                askdirectory, asksaveasfilename)
from file import File
from config import Config
from myexception import *


class UI:
    _instance = None
    __first_init = False

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        if not self.__first_init:
            self.__first_init = True
            self.__window = tk.Tk()
            self.__config = Config().get()

            self.__window.rowconfigure(0, weight=0)
            self.__window.rowconfigure(1, weight=1)
            self.__window.rowconfigure(2, weight=0)
            self.__window.rowconfigure(3, weight=0)
            self.__window.columnconfigure(0, weight=1)
            # self.__window.columnconfigure(1, weight=1)

            self.__init_nav_frame()
            self.__init_listbox_frame()
            self.__init_filter_frame()
            self.__init_Go_frame()

            # 进入消息循环
            self.__window.mainloop()

    def __init_nav_frame(self):
        self.__nav_frame = tk.Frame(self.__window)

        self.__nav_frame.rowconfigure(0, weight=0)
        self.__nav_frame.rowconfigure(1, weight=1)
        # self.__nav_frame.columnconfigure(0, weight=0)
        self.__nav_frame.columnconfigure(1, weight=1, minsize=250)
        # self.__nav_frame.columnconfigure(2, weight=0)

        self.__src_label = tk.Label(self.__nav_frame, text='筛选路径', width=10)
        self.__src_label.grid(row=0, column=0, sticky=tk.W)
        self.__dst_label = tk.Label(self.__nav_frame, text='目标路径', width=10)
        self.__dst_label.grid(row=1, column=0, sticky=tk.W)

        self.__src_path = tk.StringVar()
        self.__dst_path = tk.StringVar()
        self.__src_entry = tk.Entry(self.__nav_frame,
                                    textvariable=self.__src_path)
        self.__src_entry.bind('<FocusOut>', self.__src_listbox_update_event)
        self.__src_entry.grid(row=0, column=1, sticky=tk.EW)
        self.__dst_entry = tk.Entry(self.__nav_frame,
                                    textvariable=self.__dst_path)
        self.__dst_entry.grid(row=1, column=1, sticky=tk.EW)

        self.__src_button = tk.Button(self.__nav_frame,
                                      text="筛选路径",
                                      command=self.__src_select)
        self.__src_button.grid(row=0, column=2)

        self.__dst_button = tk.Button(self.__nav_frame,
                                      text="目标路径",
                                      command=self.__dst_select)
        self.__dst_button.grid(row=1, column=2)
        self.__nav_frame.grid(row=0, column=0, sticky=tk.W + tk.E)

    def __init_listbox_frame(self):
        self.__listbox_frame = tk.Frame(self.__window)

        self.__listbox_frame.rowconfigure(0, weight=1, minsize=350)
        self.__listbox_frame.columnconfigure(0, weight=1, minsize=250)
        self.__listbox_frame.columnconfigure(1, weight=1, minsize=250)

        self.__src_list_itmes = tk.StringVar()
        self.__src_listbox = tk.Listbox(self.__listbox_frame,
                                        listvariable=self.__src_list_itmes)
        self.__src_listbox.grid(row=0, column=0, padx=10, sticky=tk.NSEW)
        self.__filter_list_itmes = tk.StringVar()
        self.__filter_listbox = tk.Listbox(
            self.__listbox_frame, listvariable=self.__filter_list_itmes)
        self.__filter_listbox.grid(row=0, column=1, padx=10, sticky=tk.NSEW)
        self.__listbox_frame.grid(row=1, column=0, sticky=tk.NSEW)

    def __init_filter_frame(self):
        self.__filter_frame = tk.Frame(self.__window)

        self.__minsize_label = tk.Label(self.__filter_frame,
                                        text='最小文件大小(KB)：')
        self.__minsize_label.grid(row=0, column=0, sticky=tk.W)
        self.__maxsize_label = tk.Label(self.__filter_frame,
                                        text='最大文件大小(KB)：')
        self.__maxsize_label.grid(row=1, column=0, sticky=tk.W)
        self.__ext_filter_label = tk.Label(self.__filter_frame, text='扩展名筛选：')
        self.__ext_filter_label.grid(row=2, column=0, sticky=tk.W)
        self.__iteration_label = tk.Label(self.__filter_frame, text='迭代：')
        self.__iteration_label.grid(row=3, column=0, sticky=tk.W)

        self.__minsize = tk.StringVar()
        self.__maxsize = tk.StringVar()
        self.__ext_filter = tk.StringVar()
        self.__minsize.set(self.__config['min_size'])
        self.__maxsize.set(self.__config['max_size'])
        self.__ext_filter.set(" ".join(self.__config['default_ext']))
        self.__minsize_entry = tk.Entry(self.__filter_frame,
                                        textvariable=self.__minsize)
        self.__minsize_entry.grid(row=0, column=1, sticky=tk.W)
        self.__maxsize_entry = tk.Entry(self.__filter_frame,
                                        textvariable=self.__maxsize)
        self.__maxsize_entry.grid(row=1, column=1, sticky=tk.W)
        self.__ext_filter_entry = tk.Entry(self.__filter_frame,
                                           textvariable=self.__ext_filter,
                                           width=50)
        self.__ext_filter_entry.grid(row=2, column=1, sticky=tk.W)

        self.__iteration_radio_frame = tk.Frame(self.__filter_frame)
        self.__iteration = tk.IntVar()
        self.__iteration_radio_yes = tk.Radiobutton(
            self.__iteration_radio_frame,
            text='是',
            value=1,
            variable=self.__iteration,
            command=self.__src_listbox_update)
        self.__iteration_radio_no = tk.Radiobutton(
            self.__iteration_radio_frame,
            text='否',
            value=0,
            variable=self.__iteration,
            command=self.__src_listbox_update)
        self.__iteration.set(1 if self.__config['iteration'] else 0)
        self.__iteration_radio_yes.grid(row=0, column=1, sticky=tk.W)
        self.__iteration_radio_no.grid(row=0, column=2, sticky=tk.W)
        self.__iteration_radio_frame.grid(row=3, column=1, sticky=tk.W)

        self.__filter_button = tk.Button(self.__filter_frame,
                                         text='筛选',
                                         command=self.__filter,
                                         width=10)
        self.__filter_button.grid(row=0, rowspan=4, column=2, sticky=tk.NSEW)

        self.__filter_frame.grid(row=2, column=0, sticky=tk.W)

    def __init_Go_frame(self):
        self.__Go_frame = tk.Frame(self.__window)

        self.__Go_frame.rowconfigure(0, weight=1)
        self.__Go_frame.columnconfigure(0, weight=1)

        self.__Go_button = tk.Button(self.__Go_frame,
                                     text='开始迁移',
                                     command=self.__go_move)
        self.__Go_button.grid(row=0, column=0, sticky=tk.EW)

        self.__Go_frame.grid(row=3, column=0, sticky=tk.NSEW)

    def __src_listbox_update(self):
        check, _, _, _, iteration = self.__format_check()
        if check:
            self.__src_list_itmes.set(
                tuple(File.get_list(self.__src_path.get(),
                                    iteration=iteration)))
            self.__src_listbox.update()

    def __dst_listbox_update(self):
        check, minsize, maxsize, ext_filter, iteration = self.__format_check()
        if check:
            print(self.__format_check())
            self.__filter_list_itmes.set(
                tuple(
                    File.get_list(self.__src_path.get(), (minsize, maxsize),
                                  ext_filter, iteration)))
            self.__filter_listbox.update()

    def __src_select(self):
        self.__src_path.set(askdirectory())
        self.__src_entry.update()
        self.__src_listbox_update()

    def __dst_select(self):
        self.__dst_path.set(askdirectory())
        self.__dst_entry.update()

    def __format_check(self) -> tuple[bool, int, int, list[str], bool]:
        try:
            try:
                minsize = int(self.__minsize.get())
            except:
                raise minsizeException
            try:
                maxsize = int(self.__maxsize.get())
                if maxsize < minsize and maxsize != -1:
                    raise maxsizeException
            except:
                raise maxsizeException
            try:
                ext_filter = self.__ext_filter.get().split()
            except:
                raise extFilterException
            try:
                iteration = int(self.__iteration.get())
                if iteration not in (1, 0):
                    raise iterationSelectException
                iteration_bool = True if iteration == 1 else False
            except:
                raise iterationSelectException
            return (True, minsize, maxsize, ext_filter, iteration_bool)
        except minsizeException:
            tk.messagebox.showerror('错误', '最小值输入不合法')
            return (False, 0, 0, [], False)
        except maxsizeException:
            tk.messagebox.showerror('错误', '最大值输入不合法')
            return (False, 0, 0, [], False)
        except extFilterException:
            tk.messagebox.showerror('错误', '扩展名输入不合法')
            return (False, 0, 0, [], False)
        except iterationSelectException:
            tk.messagebox.showerror('错误', '迭代输入不合法')
            return (False, 0, 0, [], False)

    def __filter(self):
        self.__dst_listbox_update()

    def __go_move(self):
        check, minsize, maxsize, ext_filter, iteration = self.__format_check()
        if check:
            try:
                if File.list_move_to(
                        File.get_list(self.__src_path.get(),
                                      (minsize, maxsize), ext_filter,
                                      iteration), self.__dst_path.get()):
                    tk.messagebox.showinfo('成功', '迁移成功')
                    self.__src_listbox_update()
                    self.__dst_listbox_update()

            except dstPathException:
                tk.messagebox.showerror('错误', '迁移到目标路径时出错，可能是目标路径不合法')

    def __src_listbox_update_event(self, event):
        self.__src_listbox_update()


UI()