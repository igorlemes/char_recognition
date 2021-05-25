FROM python:latest

RUN apt-get update
RUN apt-get -y install \
    tesseract-ocr \
    tesseract-ocr-por \
    tesseract-ocr-eng \
    libgl1-mesa-dev; 
RUN apt-get clean

RUN pip3 install --upgrade pip; \
    pip3 install \
    pillow \
    opencv-python \
    pytesseract

COPY . /
# RUN pip3 install -r /requirements.txt
ENTRYPOINT ["python3", "/char_rec.py"]