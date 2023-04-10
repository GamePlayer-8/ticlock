#!/bin/sh

TZ="Europe/Warsaw"
DEBIAN_FRONTEND=noninteractive

apt update
apt install --yes markdown
cd /source

echo '<!DOCTYPE html>' > index.html
echo '<html lang="en-US">' >> index.html
cat docs/head.html >> index.html

echo '<body>' >> index.html
markdown README.md >> index.html
echo '</body>' >> index.html
echo '</html>' >> index.html

apt install --yes podman apt-utils git

py_deps_ticlock=""
for X in $(cat requirements.txt); do
    py_deps_ticlock=$py_deps_ticlock' --collect-all '$X
done

mkdir log
touch log/ticlock-main.txt

for X in $(find . -name '__pycache__'); do
    rm -rf "$X"
done

git clone https://github.com/kicsikrumpli/wine-pyinstaller /wine
podman build -t wine/pyinstaller /wine

podman run -it -v $(pwd):/src kicsikrumpli/wine-pyinstaller -F --onefile --console \
 --additional-hooks-dir=. --add-data config.py:config.py --add-data modules/*:modules/ --add-data apps/*:apps/ \
  $py_deps_ticlock --add-data log/*:log/ -i docs/icon.png -n ticlock -c main.py



mv dist/ticlock.exe .
rm -rf dist build log

chmod +x ticlock.exe

sha256sum ticlock.exe > sha256sum.txt

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/