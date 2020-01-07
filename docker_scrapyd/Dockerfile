FROM python:3.6
COPY . /app
COPY ./scrapyd.conf /etc/scrapyd/
WORKDIR /app
EXPOSE 6800
RUN pip3 install -r requirements.txt --index-url https://mirrors.aliyun.com/pypi/simple/
CMD ["scrapyd"]