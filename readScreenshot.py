from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import pytesseract
import re
import cv2
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
plt.style.use('dark_background')


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

time_re = re.compile(r'''
        (\d{2})
        .*?
        (\d{2})
        .*?
        (\d{2})
        ''', re.VERBOSE)






def extractionData(image_name_list, root=None):
    list = []

    for img_name in image_name_list:
        img_original = cv2.imread(img_name)

        height, width, channel = img_original.shape

        img_gray = cv2.cvtColor(img_original, cv2.COLOR_RGBA2GRAY)

        img_blurred = cv2.GaussianBlur(img_gray, ksize=(7,7),sigmaX=1.1)

        # img_thresh = cv2.adaptiveThreshold(
        #     img_blurred,
        #     maxValue=255.0,
        #     adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #     thresholdType=cv2.THRESH_BINARY,
        #     blockSize=49,
        #     C=13
        # )
        _, img_thresh = cv2.threshold(img_blurred, 120, 255, cv2.THRESH_BINARY)

        # plt.figure(figsize=(11, 7))
        # plt.imshow(img_thresh, cmap='gray')
        #
        # plt.show()

        contours, _= cv2.findContours(img_thresh, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

        temp_img = np.zeros((height,width,channel),dtype=np.uint8)
        # cv2.drawContours(temp_img,contours=contours,contourIdx=-1,color=(255,255,255))

        img_croped_level = cv2.getRectSubPix(
            img_gray,
            patchSize=(150, 30),
            center=(230, 115)
        )

        # img_croped_level = cv2.GaussianBlur(img_croped_level, (1,1), 0)
        #
        # # _, img_croped_level_trh = cv2.threshold(img_croped_level, 105, 255, cv2.THRESH_BINARY_INV)
        # img_croped_level_trh = cv2.adaptiveThreshold(
        #         img_croped_level,
        #         maxValue=255.0,
        #         adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #         thresholdType=cv2.THRESH_BINARY,
        #         blockSize=19,
        #         C=5
        #     )
        # contours, hierachy = cv2.findContours(img_croped_level_trh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        #
        # rects = [cv2.boundingRect(each) for each in contours]
        #
        # rects=sorted(rects, key=lambda x: x[2]+x[3] )
        # thinkness = abs(rects[0][2] - rects[1][2])*2
        #
        # # cv2.drawContours(img_croped_level, contours, -1, (255,255,255))
        #
        # for rect in rects:
        #     print(rect)
        #     cv2.circle(img_croped_level, (rect[0],rect[1]), 1, (255,255,255),-1)
        #     cv2.circle(img_croped_level, (rect[0]+rect[2], rect[1]+rect[3]), 1, (255,255,255),-1)
        #     cv2.rectangle(img_croped_level, (rect[0],rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (255,255,255), 1)
        #

        img_croped_quest = cv2.getRectSubPix(
            img_gray,
            patchSize=(400, 50),
            center=(300, 155)
        )

        img_croped_time = cv2.getRectSubPix(
            img_thresh,
            patchSize=(250, 40),
            center=(395, 300)
        )

        # img_croped_time = cv2.GaussianBlur(img_croped_time,
        #                                     ksize=(1,1),sigmaX=0)
        # _,img_croped_time = cv2.threshold(img_croped_time,
        #                                    thresh=100,
        #                                    maxval=255.0,
        #                                    type=cv2.THRESH_BINARY)
        # img_croped_time = cv2.copyMakeBorder(img_croped_time,
        #                                       top=1,
        #                                       bottom=1,
        #                                       left=1,
        #                                       right=1,
        #                                       borderType=cv2.BORDER_CONSTANT,
        #                                       value=(0,0,0))

        # level_text = pytesseract.image_to_string(img_croped_level, lang='eng')
        # print(level_text)
        #
        # plt.figure(figsize=(11,7))
        # plt.imshow(img_croped_level, cmap='gray')
        #
        # plt.show()

        text = pytesseract.image_to_string(img_croped_quest, lang='kor')
        text = text.replace('\n', '')
        # print(text)
        test_text = pytesseract.image_to_string(img_croped_time, lang=None)
        time_text = re.sub(r'[^0-9]','',test_text)
        # print(time_text)

        if len(time_text) > 5:
            clear_time = datetime.datetime.strptime(time_text, '%M%S%f')
            # time_text = clear_time.strftime('%M:%S:') + clear_time.strftime('%f')[:2]
            # print(time_text)
            path = root + '/' + str(text)
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            time_text = clear_time.strftime('%M분 %S초 ') + clear_time.strftime('%f')[:2]
            final_path = path + '/' + text + ' ' + time_text + '.jpg'
            result, encoded_img_ori = cv2.imencode('.jpg', img_original)
            if result:
                with open(final_path, mode='w+b') as f:
                    encoded_img_ori.tofile(f)

            now_day = datetime.datetime.now()
            data = [text, clear_time, final_path, now_day]
            list.append(data)

        else:
            path = root + '/분류실패'
            try:
                os.makedirs(path)
            except OSError:
                if not os.path.isdir(path):
                    raise
            now_time = datetime.datetime.now()
            final_path = path + '/' + now_time.strftime('%Y%m%d%H%M%S_1.jpg')
            result, encoded_img_ori = cv2.imencode('.jpg', img_original)
            if result:
                with open(final_path, mode='w+b') as f:
                    encoded_img_ori.tofile(f)



    return list




if __name__ == '__main__':
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

    extractionData(image_list[:1])
