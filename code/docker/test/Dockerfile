# This is a comment
FROM ubuntu
MAINTAINER me@gmail.com
RUN apt-get -y update && apt-get install -y unzip \
 python2.7
RUN mkdir /usr/test/
COPY pyusb-1.0.0a2.zip /usr/test/
COPY sympy-0.7.6.1.win32.exe /usr/test/
COPY dockerfile.txt /usr/test/
RUN unzip /usr/test/pyusb-1.0.0a2.zip -d /usr/test/
#RUN python2.7 /usr/test/pyusb-1.0.0a2/setup.py install
CMD ["/usr/test/sympy-0.7.6.1.win32.exe"]
