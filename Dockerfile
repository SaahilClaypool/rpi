# escape=`
FROM ubuntu:bionic

# build essentials
RUN apt -q -y update && apt -q -y install git bc build-essential kmod flex bison libssl-dev libncurses5-dev qt4-default qt4-dev-tools

# raspberry pi cross compile toolchains
RUN git clone https://github.com/raspberrypi/tools ~/tools

COPY ./build_cmd.sh /root/

ENV PATH="/root/tools/arm-bcm2708/gcc-linaro-arm-linux-gnueabihf-raspbian-x64/bin:${PATH}"
ENV OUT "/out"