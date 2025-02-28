from cnocr import CnOcr
from easyocr import Reader

if __name__ == '__main__':
    ocr = CnOcr()
    text = ocr.ocr('output.png')
    print(text)

    reader = Reader(['en'])
    result = reader.readtext('output.jpg')
    for line in result:
        print(line[1])