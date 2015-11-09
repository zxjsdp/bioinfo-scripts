# -*- coding: utf-8 -*-

import os
import sys
from Tkinter import *
import ttk
from ScrolledText import *


CURRENT_PATH = os.path.abspath('.')
DATA_PAHT = os.path.join(CURRENT_PATH, 'data')
SUMMARY_LINE = 10


def clean_list(orig_list):
    return [_.strip() for _ in orig_list]


class CSV_Dict(object):
    def __init__(self, detailed_list):
        self.detailed_list = detailed_list

    @classmethod
    def from_raw_data(cls, data_file):
        if not os.path.isfile(data_file):
            sys.stderr.write('>>>>> [Error]: Data file does not exist: %s\n' %
                             data_file)
        with open(data_file, 'r') as f:
            lists = clean_list(f.readlines())

        return cls(lists)

    @staticmethod
    def get_query_list(query_raw_data):
        if not query_raw_data:
            sys.stderr.write('>>>>> [Error]: No query\n')
        if ',' in query_raw_data:
            split_symbol = ','
        elif ';' in query_raw_data:
            split_symbol = ';'
        else:
            split_symbol = '\n'
        query_list = [_.strip() for _ in query_raw_data.split(split_symbol) if
                      _.strip()]
        return query_list

    @property
    def detailed_dict(self):
        detailed_dict = {}
        if ('\t' in self.detailed_list[1]
                and self.detailed_list[1].count('\t')
                == self.detailed_list[2].count('\t')):
            split_symbol = '\t'
        else:
            split_symbol = ','
        for i, line in enumerate(self.detailed_list):
            first_column, symbol, other = line.partition(split_symbol)
            first_column = first_column.strip()
            detailed_dict[first_column] = line if '\t' not in line\
                else line.replace('\t', ',')
        return detailed_dict

    @staticmethod
    def do_query(query_list, detailed_dict):
        out_list = []
        total_count = len(query_list)
        found = 0
        for i, query in enumerate(query_list):
            if query in detailed_dict:
                print('--> [%s]  Found:  %s' % (i, query))
                found += 1
                out_list.append(detailed_dict[query])
            else:
                out_list.append('%s,' % query)
                sys.stderr.write('>>> [%s]  Not Found:  %s\n' %
                                 (i, query))
        print('\n' + '=' * 52)
        print('[Found]:  %s / %s' % (found, total_count))
        print('[Found Percentage]:  %% %d' % (100.0 * found / total_count))
        with open('out.csv', 'w') as f:
            f.write('\n'.join(out_list))
            print('[Written]: out.csv')


class TextEmit(object):
    def __init__(self, widget, tag='stdout'):
        self.widget = widget
        self.tag = tag

    def write(self, out_str):
        self.widget.configure(state='normal')
        self.widget.insert('end', out_str, (self.tag,))
        self.widget.tag_configure('stderr', foreground='red',
                                  background='yellow')
        self.widget.configure(state='disabled')
        self.widget.see('end')


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.set_style()
        self.master.grid()
        self.create_widgets()
        sys.stdout = TextEmit(self.st2, 'stdout')
        sys.stderr = TextEmit(self.st2, 'stderr')
        self.cached_dict_of_dict = {}

    def set_style(self):
        s = ttk.Style()
        s.configure('TButton', padding=(5))
        s.configure('TCombobox', padding=(5))
        s.configure('exe.TButton', foreground='red')

    def parse_data(self):
        data_file = self.com.get()
        print('\n[Data File]: %s' % data_file)
        print('=' * 52)
        user_input = self.st1.get('0.1', 'end-1c')
        query_list = CSV_Dict.get_query_list(user_input)
        if data_file and query_list:
            if data_file not in self.cached_dict_of_dict:
                c = CSV_Dict.from_raw_data(os.path.join(DATA_PAHT,
                                                        data_file))
                current_dict = c.detailed_dict
                self.cached_dict_of_dict[data_file] = current_dict
            else:
                current_dict = self.cached_dict_of_dict[data_file]
            print('[Dictionary count]: %s\n' % len(current_dict.keys()))
            print('\n' + '=' * 52)
            CSV_Dict.do_query(query_list, current_dict)
            print('===== [Mission Complete] =====\n')
        else:
            sys.stderr.write('----- [Mission Failed] -----\n')
            print('\n')

    def clear_output(self):
        self.st2.configure(state='normal')
        self.st2.delete('1.0', 'end')
        self.st2.configure(state='disabled')

    def show_summary_of_data_file(self):
        data_file = os.path.join(DATA_PAHT, self.com.get())
        base_name = self.com.get()
        if not os.path.isfile(data_file):
            sys.stderr.write('>>>>> [Error]: Data file does not exist: %s\n' %
                             data_file)
        print('\n[Show Data File Summary]  %s' % base_name)
        print('=' * 52)
        with open(data_file, 'r') as f:
            for i, line in enumerate(f):
                if i < SUMMARY_LINE:
                    print('[ %d ] %s' % (i, line.strip()))
                else:
                    print('[ 10] ... ...')
                    print('[...] ... ...')
                    break

    def create_widgets(self):
        self.content = ttk.Frame(self.master, padding=(5))

        self.b1 = ttk.Button(self.content, text='Clear Query')
        self.combo_value = StringVar()
        self.com = ttk.Combobox(self.content, textvariable=self.combo_value,
                                state='readonly')
        if not os.path.isdir(DATA_PAHT):
            os.mkdir(data_folder)
        self.com['values'] = os.listdir(DATA_PAHT)
        if len(self.com['values']) > 0:
            self.com.current(0)
        else:
            sys.stderr.write('Please put csv data file in data folder and '
                             'restart this program.')
        self.b2 = ttk.Button(self.content, text='Data Summary',
                             command=self.show_summary_of_data_file)
        self.b3 = ttk.Button(self.content, text='Query', style='exe.TButton')
        self.b4 = ttk.Button(self.content, text='Clear Log')
        self.st1 = ScrolledText(self.content)
        self.st2 = ScrolledText(self.content)

        self.b1.grid(row=0, column=0, sticky=(W))
        self.b2.grid(row=0, column=1, sticky=(E))
        self.com.grid(row=0, column=1, sticky=(W+E))
        self.b3.grid(row=0, column=2, sticky=(W))
        self.b4.grid(row=0, column=3, sticky=(E))
        self.st1.grid(row=1, column=0, columnspan=2, sticky=(W+E+S+N))
        self.st2.grid(row=1, column=2, columnspan=2, sticky=(W+E+S+N))
        self.content.grid(row=0, column=0, sticky=(W+E+S+N))

        self.b1['command'] = lambda: self.st1.delete('0.1', 'end')
        self.b3['command'] = self.parse_data
        self.b4['command'] = self.clear_output

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.content.rowconfigure(0, weight=0)
        self.content.rowconfigure(1, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.columnconfigure(1, weight=1)
        self.content.columnconfigure(2, weight=1)
        self.content.columnconfigure(3, weight=1)

        self.st1.focus()


def main():
    app = App()
    app.master.title('Dictionary')
    app.master.geometry('1100x600')
    app.mainloop()


if __name__ == '__main__':
    main()
