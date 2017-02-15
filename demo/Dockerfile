FROM i686/ubuntu
MAINTAINER me@gmail.com
RUN apt-get -y update && apt-get install -y
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*

RUN mkdir /usr/test/
COPY QtInstallerFramework-linux-x86.run /usr/test/
COPY qt-installer-framework-opensource-2.0.3-src.tar.gz /usr/test/
COPY qt-unified-linux-x64-2.0.5-online.run /usr/test/
COPY testpython.py /usr/test
#tar -zxvf file.tar.gz