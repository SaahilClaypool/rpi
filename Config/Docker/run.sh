docker build . -t saahil/rpi_build

docker run --rm \
    -v /home/saahil/raspberry/rpi-full-source-19:/linux \
    -v /home/saahil/raspberry/out:/out \
    -e _UID=`id -u` \
    -e _GID=`id -g` \
    -it saahil/rpi_build sh /root/build_cmd.sh
