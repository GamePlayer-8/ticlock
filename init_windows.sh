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
    py_deps_ticlock=$py_deps_ticlock' --collect-all "'$X'"'
done

mkdir log
touch log/ticlock-main.txt

for X in $(find . -name '__pycache__'); do
    rm -rf "$X"
done

export WINEPREFIX=/wine
export DISPLAY=":0"
export WINEDEBUG="-all"
export PYTHON_VERSION=3.11.3
export UPX_VERSION=3.96
export WINEDLLOVERRIDES="winemenubuilder.exe,mscoree,mshtml="

Xvfb -ac :0 -screen 0 1280x1024x24 &
sleep 5

xvfb-run sh -c "wine reg add 'HKLM\Software\Microsoft\Windows NT\CurrentVersion' /v CurrentVersion /d 10.0 /f && \
wine reg add 'HKCU\Software\Wine\DllOverrides' /v winemenubuilder.exe /t REG_SZ /d '' /f && \
wine reg add 'HKCU\Software\Wine\DllOverrides' /v mscoree /t REG_SZ /d '' /f && \
wine reg add 'HKCU\Software\Wine\DllOverrides' /v mshtml /t REG_SZ /d '' /f; \
wineserver -w"

wget -q https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-amd64.exe -O /python-${PYTHON_VERSION}-amd64.exe
wget -q https://github.com/upx/upx/releases/download/v${UPX_VERSION}/upx-${UPX_VERSION}-win64.zip -O /upx-${UPX_VERSION}-win64.zip

cd /

xvfb-run sh -c "\
    wine /python-${PYTHON_VERSION}-amd64.exe /quiet TargetDir=C:\\Python310 \
      Include_doc=0 InstallAllUsers=1 PrependPath=1; \
    wineserver -w" && \
  unzip upx*.zip && \
  mv -v upx*/upx.exe ${WINEPREFIX}/drive_c/windows/

export WINEPATH='C:\Python310\Scripts'

wine python -m pip install --upgrade setuptools wheel pip
wine python -m pip install pyinstaller

cd /source

wine python -m pip install -r requirements.txt

wine pyinstaller $py_deps_ticlock --add-data 'log/*;log/' --add-data 'config.py;config.py' --add-data 'modules/*;modules/' --add-data 'apps/*;apps/' \
  -F --onefile --console \
  --additional-hooks-dir=. \
  -i 'docs/icon.ico' -n ticlock -c main.py

mv dist/ticlock.exe .
rm -rf dist build log

chmod +x ticlock.exe

sha256sum ticlock.exe > sha256sum.txt

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/