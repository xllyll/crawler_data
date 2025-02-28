from cnocr import CnOcr

if __name__ == '__main__':
    ocr = CnOcr()
    text = ocr.ocr('test.png')
    print(text)