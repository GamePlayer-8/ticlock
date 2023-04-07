#!/bin/sh

apk add --no-cache markdown
cd /source

echo '<!DOCTYPE html>' > index.html
echo '<html lang="en-US">' >> index.html
cat docs/head.html >> index.html

echo '<body>' >> index.html
markdown README.md >> index.html
echo '</body>' >> index.html
echo '</html>' >> index.html

apk add --no-cache py-pip linux-headers build-base python3-dev xrdp xorgxrdp

# FIX CERTIFICATES
for X in $(find /usr -name *.pem); do
    rm -f "$X"
    ln -s /etc/ssl/cert.pem "$X"
done

pip install --upgrade wheel setuptools
pip install -r requirements.txt
pip install pyinstaller

# FIX CERTIFICATES
for X in $(find /usr -name *.pem); do
    rm -f "$X"
    ln -s /etc/ssl/cert.pem "$X"
done

rc-service xrdp start
rc-service xrdp-sesman start

DISPLAY=":0" pyinstaller -D -F -n ticlock -c main.py

rc-service xrdp-sesman stop
rc-service xrdp stop

mv dist/ticlock .
rm -rf dist build 

mkdir -v /runner/page/
cp -rv /source/* /runner/page/