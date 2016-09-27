# This is a comment
FROM ubuntu
MAINTAINER me@gmail.com
RUN apt-get -y update && apt-get install -y unzip \
 python2.7
RUN mkdir /usr/test/
COPY pyusb-1.0.0a2.zip /usr/test/
COPY sympy-0.7.6.1.win32.exe /usr/test/
RUN unzip /usr/test/pyusb-1.0.0a2.zip -d /usr/test/
CMD ["/usr/test/sympy-0.7.6.1.win32.exe"]