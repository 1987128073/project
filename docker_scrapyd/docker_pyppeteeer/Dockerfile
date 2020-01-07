FROM python:3.6
RUN yum -y install git libX11-xcb pango libXcomposite libXcursor libXdamage libXext libXi libXtst cups-libs libXScrnSaver libXrandr GConf2 alsa-lib atk gtk3 nss -y && yum -y install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
COPY ./zhiboshuju_all_data/ /app
WORKDIR /app
RUN pip install -r requirements.txt --index-url https://mirrors.aliyun.com/pypi/simple/
CMD ["python","dsj_chrome.py"]