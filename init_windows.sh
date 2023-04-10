#!/bin/sh

TZ="Europe/Warsaw"
DEBIAN_FRONTEND=noninteractive

apt update > /dev/null
apt install --yes markdown > /dev/null
cd /source

echo '<!DOCTYPE html>' > index.html
echo '<html lang="en-US">' >> index.html
cat docs/head.html >> index.html

echo '<body>' >> index.html
markdown README.md >> index.html
echo '</body>' >> index.html
echo '</html>' >> index.html

apt install --yes wine apt-utils tar wget xvfb winetricks > /dev/null
dpkg --add-architecture i386 && apt-get update > /dev/null && apt-get install --yes wine32 > /dev/null

py_deps_ticlock=""
for X in $(cat requirements.txt); do
    py_deps_ticlock=$py_deps_ticlock' --collect-all '$X
done

mkdir log
touch log/ticlock-main.txt

for X in $(find . -name '__pycache__'); do
    rm -rf "$X"
done

export WINEPREFIX=/wine
export DISPLAY=":0"

wget -q https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -O /installer.exe

chown -R $(whoami):$(whoami) /github

Xvfb -ac :0 -screen 0 1280x1024x24 &
sleep 5

wine /installer.exe /quiet
PYTHON_EXE_FILE=$(find /wine -name python.exe | tail -n 1)
wine $PYTHON_EXE_FILE -m pip install --upgrade setuptools wheel > /dev/null
wine $PYTHON_EXE_FILE -m pip install pyinstaller > /dev/null
wine $PYTHON_EXE_FILE -m pip install -r requirements.txt > /dev/null

wine $PYTHON_EXE_FILE -m pyinstaller -F --onefile --console \
 --additional-hooks-dir=. --add-data ./config.py;config.py --add-data ./modules/*;modules/ --add-data ./apps/*;apps/ \
  $py_deps_ticlock --add-data ./log/*;log/ -i ./docs/icon.png -n ticlock -c main.py

mv dist/ticlock.exe .
rm -rf dist build log

chmod +x ticlock.exe

sha256sum ticlock.exe > sha256sum.txt

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/