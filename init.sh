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

apk add --no-cache py-pip linux-headers build-base python3-dev xvfb

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

Xvfb -ac :0 -screen 0 1280x1024x24 &
sleep 5

py_deps_ticlock=""
for X in $(cat requirements.txt); do
    py_deps_ticlock=$py_deps_ticlock' --collect-all '$X
done

mkdir log
touch log/ticlock-main.txt

mkdir cache
cp -r /usr/lib/python3.10/site-packages/* cache/

py_modules_ticlock=""
for X in $(ls cache); do
    py_modules_ticlock=$py_modules_ticlock' --add-data cache/'$X'/*:'$X'/'
done

DISPLAY=":0" pyinstaller -F --onefile --console \
 --additional-hooks-dir=. --add-data modules/*:modules/ --add-data apps/*:apps/ \
  $py_deps_ticlock $py_modules_ticlock --add-data log/*:log/ -n ticlock -c main.py

mv dist/ticlock .
rm -rf dist build log cache
strip ticlock

mkdir -v /runner/page/
cp -rv /source/* /runner/page/