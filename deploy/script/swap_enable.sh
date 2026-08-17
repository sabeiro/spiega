sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
#sudo cp /etc/fstab /etc/fstab.bak
#sudo vim /etc/fstab
