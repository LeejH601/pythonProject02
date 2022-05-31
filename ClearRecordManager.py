import readScreenshot
from collections import defaultdict


clear_record = defaultdict(list)

image_list = [
    '20201005165215_1.jpg',
    '20201007141333_1.jpg',
    '20210314225429_1.jpg',
    '20211112013437_1.jpg',
    '20220530213953_1.jpg',
    '20220530225418_1.jpg'
    ]

def insertData(data):
    clear_record[data[0]].append(data[1])


if __name__ == '__main__':
    data_list = readScreenshot.extractionData(image_list)
    for data in data_list:
        insertData(data)

    for quest_name, times in clear_record.items():
        for time in times:
            print(quest_name, time)