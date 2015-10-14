#a=("/sdcard" "/sdcard/bluetooth" "/sdcard/WhatsApp/Profile Pictures/" "/sdcard/airdroid")
func(){
local directory=$1
for i in $directory/*
do
if [ -d "$i" ]
then
func $i
else
echo "$i" >> /sdcard/a.txt
fi
done
}

for each in $*
do
func $each
done
