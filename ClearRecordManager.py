import readScreenshot
from collections import defaultdict
import json
import datetime
import os
import cv2


clear_record = defaultdict(list)

image_list = [
    '20201005165215_1.jpg',
    '20201007141333_1.jpg',
    '20210314225429_1.jpg',
    '20211112013437_1.jpg',
    '20220530213953_1.jpg',
    '20220530225418_1.jpg',
    '20220601015325_1.jpg',
    '20220601020827_1.jpg',
    '20220601021930_1.jpg',
    '20220601023309_1.jpg'
    ]

def insertData(data):
    clear_record[data[0]].append([data[1],data[2],data[3]])


def extractScreenshot(path, root):
    image_name_list = []
    image_name_list.append(path)
    data_list = readScreenshot.extractionData(image_name_list, root)
    for data in data_list:
        insertData(data)
    saverecord(root)

def addData(root, filename, quest, time):
    img_original = cv2.imread(filename)
    clear_time = datetime.datetime.strptime(time, '%M%S%f')
    # time_text = clear_time.strftime('%M:%S:') + clear_time.strftime('%f')[:2]
    # print(time_text)
    path = root + '/' + str(quest)
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise
    time_text = clear_time.strftime('%M분 %S초 ') + clear_time.strftime('%f')[:2]
    final_path = path + '/' + quest + ' ' + time_text + '.jpg'
    result, encoded_img_ori = cv2.imencode('.jpg', img_original)
    if result:
        with open(final_path, mode='w+b') as f:
            encoded_img_ori.tofile(f)

    now_day = datetime.datetime.now()
    data = [quest, clear_time, final_path, now_day]
    insertData(data)
    saverecord(root)

def testSetRaod(root=None):
    data_list = readScreenshot.extractionData(image_list, root)
    for data in data_list:
        insertData(data)

    for quest_name, times in clear_record.items():
        for time in times:
            print(quest_name, time)


def updateNewFolderLocate(root):
    for quest, values in clear_record.items():
        for value in values:
            time_text = value[0].strftime('%M분 %S초 ') + value[0].strftime('%f')[:2]
            final_path = root + '/' + quest + '/' + quest + ' ' + time_text + '.jpg'
            value[1] = final_path


def sortQuest(isAscending=True):
    global clear_record
    if isAscending:
        clear_record = dict(sorted(clear_record.items()))


def sortQuestByTime(isAscending=True):
    if isAscending:
        for quest, value in clear_record.items():
            value.sort(key=lambda x:x[0])
    else:
        for quest, value in clear_record.items():
            value.sort(key=lambda x:x[0],reverse=True)




def saverecord(root):
    sortQuestByTime()
    clear_record_json_format = defaultdict(list)

    for key, values in clear_record.items():
        for time, path, day in values:
            time_text = time.strftime('%M:%S:') + time.strftime('%f')[:2]
            clear_record_json_format[key].append([time_text, path, str(day)])

    try:
        os.makedirs(root)
    except OSError:
        if not os.path.isdir(root):
            raise

    path = root + '/data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(clear_record_json_format, f, indent='\t')


def loadrecord(root):
    global  clear_record

    path = root + '/data.json'
    with open(path, 'r', encoding='utf-8') as f:
        clear_record_json_format = json.load(f)

    for key, values in clear_record_json_format.items():
        for time_text, path, day in values:
            clear_time = datetime.datetime.strptime(time_text, '%M:%S:%f')
            clear_record[key].append([clear_time, path, datetime.datetime.strptime(day,'%Y-%m-%d %H:%M:%S.%f')])



if __name__ == '__main__':
    data_list = readScreenshot.extractionData(image_list)
    for data in data_list:
        insertData(data)

    # for quest_name, times in clear_record.items():
    #     for time in times:
    #         print(quest_name, time)
