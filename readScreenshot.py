from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
import pytesseract
import re


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

time_re = re.compile(r'''
        (\d{2})
        .*?
        (\d{2})
        .*?
        (\d{2})
        ''', re.VERBOSE)


def extractionData(image_name_list):
    list = []

    for img_name in image_name_list:
        img = Image.open(img_name)
        # edge_img = img.filter(ImageFilter.FIND_EDGES )

        image = img.copy()
        data = []
        crop_image = image.crop((100, 130, 500, 180))
        width, height = crop_image.size
        crop_image = crop_image.resize((width * 2, height * 2), Image.ANTIALIAS)

        gray_img = ImageEnhance.Color(crop_image).enhance(0.0)
        cont_img = ImageEnhance.Contrast(gray_img).enhance(2.0)
        # blur_img = gray_img.filter(ImageFilter.BLUR)
        edge_img = ImageEnhance.Sharpness(cont_img).enhance(2.0)

        # edge_img.show()

        text = pytesseract.image_to_string(edge_img, lang='kor')
        text = text.replace('\n', '')
        text = text.replace('.',' ')
        data.append(text)

        crop_image = image.crop((270, 270, 520, 330))
        width, height = crop_image.size
        crop_image = crop_image.resize((width * 2, height * 2), Image.ANTIALIAS)

        gray_img = ImageEnhance.Color(crop_image).enhance(0.0)
        cont_img = ImageEnhance.Contrast(gray_img).enhance(3.0)
        # blur_img = gray_img.filter(ImageFilter.BLUR)
        edge_img = ImageEnhance.Sharpness(cont_img).enhance(2.0)
        edge_img = edge_img.filter(ImageFilter.DETAIL)

        # edge_img.show()

        text = pytesseract.image_to_string(edge_img, lang='kor+eng')

        mo = time_re.search(text)
        data.append(str(mo.group(1)) + ':' + str(mo.group(2)) + ':' + str(mo.group(3)))

        list.append(data)

    return list
