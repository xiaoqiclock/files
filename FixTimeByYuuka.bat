w32tm /unregister
w32tm /register
net start w32time
w32tm /config /manualpeerlist:"ntp.ntsc.ac.cn" /syncfromflags:manual /update
w32tm /resync /force
