#a=("/sdcard" "/sdcard/bluetooth" "/sdcard/WhatsApp/Profile Pictures/" "/sdcard/airdroid")
for each in $*
do
echo "$each"
for i in $each/*
do
if ! [ -d "$i" ]
then
echo "$i" >> /sdcard/a.txt
fi
done
done
