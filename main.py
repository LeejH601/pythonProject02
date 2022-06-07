# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import datetime
import os.path
import tkinter.ttk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import ClearRecordManager as CRM
from functools import partial
from PIL import Image, ImageTk
import keyboard
import winsound
import time


def stop(event=None):
    main_window.quit()

def selectFolder_r():
    dir_name = filedialog.askdirectory()
    if dir_name:
        recodeed_address = dir_name
        address_of_record_data_entry.delete(0,END)
        address_of_record_data_entry.insert(0,recodeed_address)
        with open('./recordFolder.txt','w') as f:
            f.write(dir_name)


def selectFolder_sht():
    dir_name = filedialog.askdirectory()
    if dir_name:
        orignal_image_address = dir_name
        address_of_steamSht_entry.delete(0,END)
        address_of_steamSht_entry.insert(0,orignal_image_address)
        with open('oriFolder.txt','w') as f:
            f.write(dir_name)


def getFolder_sht():
    global orignal_image_address
    with open('oriFolder.txt', 'r') as f:
        orignal_image_address = f.read()


def getFolder_r():
    global recodeed_address
    with open('recordFolder.txt', 'r') as f:
        recodeed_address = f.read()


def open_recored_image(path):
    Image.open(path).show()


def select_clear_record(index):
    questName = quest_list[index]['text']
    for widget in time_list_frame.winfo_children():
        widget.destroy()

    row = 0
    for time, path, day in CRM.clear_record[questName]:
        time_text = time.strftime('%M:%S:') + time.strftime('%f')[:2]
        text_label = Label(time_list_frame, text=questName + ' │ ' + time_text + ' │ ' + str(day), borderwidth="1",
                     relief="solid")
        text_label.configure(background='white')
        Button(time_list_frame,image=photo_icon,width=2, command=partial(open_recored_image, path)).grid(row=row, column=0,sticky='ns')
        text_label.grid(row=row, column=1,sticky='ns')
        row += 1

    updateTimeList()

    # time_listbox.delete(0, END)
    # index = 0
    # for time in CRM.clear_record[questName]:
    #     time_text = time.strftime('%M:%S:') + time.strftime('%f')[:2]
    #     time_listbox.insert(index, questName + '\t' + time_text)
    #     index+=1
    # time_listbox.update()


def select_Sortby(event=None):
    selection = comboBox_time.get()
    if selection == '오름차순':
        CRM.sortQuestByTime(True)
    elif selection == '내림차순':
        CRM.sortQuestByTime(False)


def select_Sortby_ForQuest(event=None):
    global index, quest_list
    for widget in main_list_frame.winfo_children():
        widget.destroy()

    selection = comboBox_quest.get()
    CRM.sortQuest(True)
    # if selection == '오름차순':
    #     CRM.sortQuest(True)
    # elif selection == '내림차순':
    #     CRM.sortQuest(False)

    quest_list.clear()
    index = 0
    if selection == '오름차순':
        for quest_name in CRM.clear_record.keys():
            quest_button = Button(main_list_frame, text=quest_name, command=partial(select_clear_record, index))
            quest_button.pack(fill=X, expand=True)
            quest_list.append(quest_button)
            index += 1
    elif selection == '내림차순':
        for quest_name in list(CRM.clear_record.keys())[::-1]:
            quest_button = Button(main_list_frame, text=quest_name, command=partial(select_clear_record, index))
            quest_button.pack(fill=X, expand=True)
            quest_list.append(quest_button)
            index += 1


def start_wait_input_sound():
    winsound.Beep(440, 200)
    winsound.Beep(440, 200)


def end_wait_input_sound():
    winsound.Beep(440, 200)
    winsound.Beep(440, 200)
    winsound.Beep(440, 200)


def extractForinputScreenshot():
    winsound.Beep(400, 500)
    now_time = datetime.datetime.now()
    new_screenshot_name = now_time.strftime('%Y%m%d%H%M%S_1.jpg')
    # print(new_screenshot_name)

    path = orignal_image_address + '/' + new_screenshot_name
    # print(path)

    wait_timer = 1.0
    while True:
        if os.path.isfile(path):
            break

        time.sleep(0.3)
        wait_timer -= 0.3
        if wait_timer <= 0:
            break
    if wait_timer <= 0:
        now_time = now_time - datetime.timedelta(seconds=1)
        new_screenshot_name = now_time.strftime('%Y%m%d%H%M%S_1.jpg')
        path = orignal_image_address + '/' + new_screenshot_name
        wait_timer = 1.0

        while True:
            if os.path.isfile(path):
                break

            time.sleep(0.3)
            wait_timer -= 0.3
            if wait_timer <= 0:
                return None

    CRM.extractScreenshot(path, recodeed_address)
    select_Sortby_ForQuest()
    updateMainList()
    return True

def updateMainList():
    main_list_canvas.update_idletasks()
    main_list_canvas.configure(scrollregion=main_list_canvas.bbox("all"))

def updateTimeList():
    time_list_canvas.update_idletasks()
    time_list_canvas.configure(scrollregion=time_list_canvas.bbox("all"))

orignal_image_address = ""
recodeed_address = "C:/Proejcts/pythonProject02/my_record"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    keyboard.add_hotkey('F12', extractForinputScreenshot)
    start_wait_input_sound()

    getFolder_r()
    getFolder_sht()

    CRM.loadrecord(recodeed_address)
    # CRM.testSetRaod(recodeed_address)
    # CRM.saverecord(recodeed_address)
    # CRM.updateNewFolderLocate(recodeed_address)



    main_window = Tk()
    main_window.title('기록보관소')
    main_window.geometry('+0+0')
    main_window.resizable(False, False)
    main_window.bind('<Escape>', stop)

    photo_icon_img = Image.open('photoicon.png')
    resize_photo_img = photo_icon_img.resize((15,15))
    photo_icon = ImageTk.PhotoImage(resize_photo_img)

    folder_icon_img = Image.open('folder_icon.png')
    resize_folder_img = folder_icon_img.resize((15, 15))
    folder_icon = ImageTk.PhotoImage(resize_folder_img)

    list_frame_image = Image.open('frame1.png')
    list_resize_image = list_frame_image.resize((180, 20))
    list_Frame_icon = ImageTk.PhotoImage(list_resize_image)

    first_label_frame = LabelFrame()
    first_label_frame.pack(fill=BOTH, padx=20, pady=5)

    screenshot_label = Label(first_label_frame, text='스팀 스크린샷 폴더 위치:')
    screenshot_label.pack(side=LEFT,expand=True)

    address_of_steamSht_entry = Entry(first_label_frame, width=70)
    # data_entry.bind('<Return>', )
    address_of_steamSht_entry.pack(side=LEFT, pady=5,padx=5)
    address_of_steamSht_entry.insert(0, orignal_image_address)

    steamShtAdrs_select_Button = Button(first_label_frame, image=folder_icon, command=selectFolder_sht, width=2)
    steamShtAdrs_select_Button.pack(side=RIGHT,expand=False,padx=5,pady=2)



    second_label_frame = LabelFrame()
    second_label_frame.pack(fill=BOTH, padx=20, pady=5)

    record_data_label = Label(second_label_frame, text='저장 폴더 위치:')
    record_data_label.pack(side=LEFT,expand=True)

    recordedAdrs_select_Button = Button(second_label_frame, image=folder_icon, command=selectFolder_r, width=2)
    recordedAdrs_select_Button.pack(side=RIGHT, expand=False, padx=5, pady=2)

    address_of_record_data_entry = Entry(second_label_frame, width=70)
    # data_entry.bind('<Return>', )
    address_of_record_data_entry.pack(side=RIGHT, pady=5, padx=5)
    address_of_record_data_entry.insert(0, recodeed_address)


    main_list_Label_frame = LabelFrame(width=20, height=20)
    main_list_Label_frame.pack(side=LEFT,pady=20, padx=20)

    # main_listbox = Listbox(main_list_frame)
    # main_listbox.pack(fill=BOTH, pady=5,padx=5)
    # main_listbox.bind('<<ListboxSelect>>', select_clear_record)

    main_list_canvas = Canvas(main_list_Label_frame, height=200, width=200)


    main_list_scrollbar = tkinter.ttk.Scrollbar(
        main_list_Label_frame,
        orient=VERTICAL,
        command=main_list_canvas.yview
    )
    main_list_scrollbar_horizon = tkinter.ttk.Scrollbar(
        main_list_Label_frame,
        orient=HORIZONTAL,
        command=main_list_canvas.xview
    )
    main_list_canvas.configure(yscrollcommand=main_list_scrollbar.set)
    main_list_canvas.configure(xscrollcommand=main_list_scrollbar_horizon.set)
    main_list_canvas.bind('<Configure>', lambda x: main_list_canvas.configure(scrollregion = main_list_canvas.bbox("all")))


    def downMainListofMousewheel(event=None):
        if event.delta < 0:
            main_list_canvas.yview('scroll', 1, 'units')
        else:
            main_list_canvas.yview('scroll', -1, 'units')

    main_list_scrollbar.bind('<MouseWheel>', downMainListofMousewheel)
    main_list_scrollbar.pack(fill=Y, side=RIGHT)
    main_list_scrollbar_horizon.pack(side=BOTTOM, fill=X)
    main_list_canvas.pack()

    main_list_frame = Frame(main_list_canvas)
    main_list_canvas.create_window((0, 0), window=main_list_frame,  anchor="nw")

    quest_list = []
    index = 0
    for quest_name in CRM.clear_record.keys():
        quest_button = Button(main_list_frame,text=quest_name, command=partial(select_clear_record, index))
        quest_button.pack(fill=X, expand=True)
        quest_list.append(quest_button)
        index += 1



    time_list_Label_frame = LabelFrame()
    time_list_Label_frame.pack(side=RIGHT, pady=20, padx=20)

    time_list_canvas = Canvas(time_list_Label_frame)

    time_list_scrollbar = tkinter.ttk.Scrollbar(
        time_list_Label_frame,
        orient=VERTICAL,
        command=time_list_canvas.yview
    )
    time_list_scrollbar_horizon = tkinter.ttk.Scrollbar(
        time_list_Label_frame,
        orient=HORIZONTAL,
        command=time_list_canvas.xview
    )

    time_list_canvas.configure(yscrollcommand=time_list_scrollbar.set)
    time_list_canvas.configure(background='white')
    time_list_canvas.configure(xscrollcommand=time_list_scrollbar_horizon.set)

    def downTimeListofMousewheel(event=None):
        if event.delta < 0:
            time_list_canvas.yview('scroll', 1, 'units')
        else:
            time_list_canvas.yview('scroll', -1, 'units')

    time_list_scrollbar.pack(side=RIGHT, fill=Y)
    time_list_canvas.bind('<MouseWheel>', downTimeListofMousewheel)
    time_list_scrollbar_horizon.pack(side=BOTTOM, fill=X)
    time_list_canvas.pack()

    time_list_frame = Frame(time_list_canvas)
    time_list_canvas.create_window((0, 0), window=time_list_frame, anchor="nw")

    # time_list_canvas.bind('<Configure>', updateTimeList())

    check_box_frame = Frame(main_window)
    check_box_frame.pack(side=LEFT)

    combo_quest_label = LabelFrame(check_box_frame, text='퀘스트 정렬 기준')
    combo_quest_label.pack()
    comboBox_quest = Combobox(combo_quest_label, values=['오름차순', '내림차순'])
    comboBox_quest.pack(side=RIGHT, padx=5, pady=5)
    comboBox_quest.current(0)
    comboBox_quest.bind('<<ComboboxSelected>>', select_Sortby_ForQuest)

    combo_time_label = LabelFrame(check_box_frame, text='클리어 타임 정렬 기준')
    combo_time_label.pack()
    comboBox_time = Combobox(combo_time_label, values=['오름차순', '내림차순'])
    comboBox_time.pack(side=RIGHT,padx=5,pady=5)
    comboBox_time.current(0)
    comboBox_time.bind('<<ComboboxSelected>>', select_Sortby)


    main_window.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
