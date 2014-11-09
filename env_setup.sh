sudo apt-get update
sudo apt-get install -y git-core
sudo apt-get install -y unzip
sudo apt-get install -y libjpeg62
sudo apt-get install -y libjpeg62-dev
sudo apt-get install -y libfreetype6
sudo apt-get install -y libfreetype6-dev
sudo apt-get install -y zlib1g-dev
sudo apt-get install -y build-essential
sudo apt-get install -y python-dev
sudo apt-get install -y xvfb
sudo apt-get install -y firefox
sudo apt-get install -y x11-xserver-utils
sudo apt-get install -y python-imaging
sudo apt-get install -y scrot
sudo apt-get install -y libzmq-dev
sudo apt-get install -y supervisor
sudo apt-get install -y libjpeg 
sudo apt-get install -y libjpeg-dev
sudo apt-get install -y libjpeg-dev
sudo apt-get install -y python-pip

sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/

echo -e "pref(\"network.proxy.http\", \"64.62.233.67\");" | sudo tee -a /usr/lib/firefox/defaults/pref/vendor-gre.js 
echo -e "pref(\"network.proxy.http_port\", 80);" | sudo tee -a /usr/lib/firefox/defaults/pref/vendor-gre.js 
