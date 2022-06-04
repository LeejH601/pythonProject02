# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import ClearRecordManager as CRM
from functools import partial
from tkinter.tix import *


def stop(event=None):
    main_window.quit()

def selectFolder_r():
    dir_name = filedialog.askdirectory()
    orignal_image_address = dir_name
    address_of_record_data_entry.delete(0,END)
    address_of_record_data_entry.insert(0,orignal_image_address)


def selectFolder_sht():
    dir_name = filedialog.askdirectory()
    recodeed_address = dir_name
    address_of_steamSht_entry.delete(0,END)
    address_of_steamSht_entry.insert(0,recodeed_address)


def select_clear_record(index):
    questName = quest_list[index]['text']

    time_listbox.delete(0, END)
    index = 0
    for time in CRM.clear_record[questName]:
        time_listbox.insert(index, questName + '\t' + time)
        index+=1
    time_listbox.update()




orignal_image_address = ""
recodeed_address = "C:\Proejcts\pythonProject02\my_record"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    CRM.testSetRaod()

    main_window = Tk()
    main_window.title('기록보관소')
    main_window.geometry('+0+0')
    main_window.resizable(False, False)
    main_window.bind('<Escape>', stop)


    first_label_frame = LabelFrame()
    first_label_frame.pack(padx=20, pady=5)

    screenshot_label = Label(first_label_frame, text='스팀 스크린샷 폴더 위치:')
    screenshot_label.pack(side=LEFT)

    address_of_steamSht_entry = Entry(first_label_frame, width=70)
    # data_entry.bind('<Return>', )
    address_of_steamSht_entry.pack(side=LEFT, pady=5,padx=5)
    address_of_steamSht_entry.insert(0, orignal_image_address)

    steamShtAdrs_select_Button = Button(first_label_frame, text='...', command=selectFolder_sht, width=2)
    steamShtAdrs_select_Button.pack(side=RIGHT,expand=True,padx=5,pady=2)



    second_label_frame = LabelFrame()
    second_label_frame.pack(fill=BOTH, padx=20, pady=5)

    record_data_label = Label(second_label_frame, text='저장 폴더 위치:')
    record_data_label.pack(side=LEFT,expand=True)

    recordedAdrs_select_Button = Button(second_label_frame, text='...', command=selectFolder_r, width=2)
    recordedAdrs_select_Button.pack(side=RIGHT, expand=False, padx=5, pady=2)

    address_of_record_data_entry = Entry(second_label_frame, width=70,state=UNDERLINE)
    # data_entry.bind('<Return>', )
    address_of_record_data_entry.pack(side=RIGHT, pady=5, padx=5)
    address_of_record_data_entry.insert(0, recodeed_address)


    main_list_frame = LabelFrame(height=50)
    main_list_frame.pack(expand=True, side=LEFT, fill=BOTH, pady=5, padx=5)

    ScrolledWin
    main_list_scrollbar = tkinter.ttk.Scrollbar(
        main_list_frame,
        orient=VERTICAL,
        command=main_list_frame
    )
    main_list_scrollbar.pack(side=RIGHT, fill=BOTH)

    # main_listbox = Listbox(main_list_frame)
    # main_listbox.pack(fill=BOTH, pady=5,padx=5)
    # main_listbox.bind('<<ListboxSelect>>', select_clear_record)

    quest_list = []
    index = 0
    for quest_name in CRM.clear_record.keys():
        quest_button = Button(main_list_frame, text=quest_name, command=partial(select_clear_record, index))
        quest_button.pack(fill=BOTH)
        quest_list.append(quest_button)
        index += 1
    for quest_name in CRM.clear_record.keys():
        quest_button = Button(main_list_frame, text=quest_name, command=partial(select_clear_record, index))
        quest_button.pack(fill=BOTH)
        quest_list.append(quest_button)
        index += 1
    for quest_name in CRM.clear_record.keys():
        quest_button = Button(main_list_frame, text=quest_name, command=partial(select_clear_record, index))
        quest_button.pack(fill=BOTH)
        quest_list.append(quest_button)
        index += 1

    # index = 0
    # for quest_name in CRM.clear_record.keys():
    #     main_listbox.insert(index,quest_name)
    #     index += 1


    time_list_frame = LabelFrame()
    time_list_frame.pack(expand=True, side=LEFT, fill=BOTH, pady=5, padx=5)

    time_list_scrollbar = tkinter.ttk.Scrollbar(
        time_list_frame,
        orient=VERTICAL,
        command=YView
    )
    time_list_scrollbar.pack(side=RIGHT, fill=BOTH)

    time_listbox = Listbox(time_list_frame)
    time_listbox.pack(fill=BOTH, pady=5, padx=5)

    main_window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
