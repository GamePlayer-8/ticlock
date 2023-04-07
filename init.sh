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

DISPLAY=":0" pyinstaller -F --onefile --console \
 --additional-hooks-dir=. --add-data modules/*:modules/ --add-data apps/*:apps/ \
  $py_deps_ticlock --add-data log/*:log/ -n ticlock -c main.py

mv dist/ticlock .
rm -rf dist build log
strip ticlock

chmod +x ticlock

apk add --no-cache appstream tar

wget https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64/apk-tools-static-2.12.10-r1.apk -O installer.apk

cd /
tar -xzf /source/installer.apk
cd /source

rm -f installer.apk
/sbin/apk.static -X https://dl-cdn.alpinelinux.org/alpine/latest-stable/main -U --allow-untrusted -p /source/ticlock.AppDir/ --initdb add --no-cache alpine-base busybox

cp docs/icon.png ticlock.AppDir/icon.png

echo '[Desktop Entry]' > ticlock.AppDir/ticlock
echo 'Name=ticlock' >> ticlock.AppDir/ticlock
echo 'Description=TiClock' >> ticlock.AppDir/ticlock
echo 'Type=Application' >> ticlock.AppDir/ticlock
echo 'Icon=icon' >> ticlock.AppDir/ticlock
echo 'Terminal=true' >> ticlock.AppDir/ticlock

chmod +x ticlock.AppDir/ticlock

echo '#!/bin/sh' > ticlock.AppDir/AppRun
echo 'TICLOCK_RUNPATH="$(dirname "$(readlink -f "${0}")")"' >> ticlock.AppDir/AppRun
echo 'TICLOCK_EXEC="${TICLOCK_RUNPATH}"/usr/bin/ticlock' >> ticlock.AppDir/AppRun
echo 'exec "${TICLOCK_EXEC}" $@' >> ticlock.AppDir/AppRun

chmod +x ticlock.AppDir/AppRun

mkdir -p ticlock.AppDir/usr/bin
cp ticlock ticlock.AppDir/usr/bin/
chmod +x ticlock.AppDir/usr/bin/ticlock

wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O toolkit.AppImage
chmod +x toolkit.AppImage

ARCH=x86_64 /source/toolkit.AppImage ticlock.AppDir/

rm -rf ticlock.AppDir
rm -f toolkit.AppImage
chmod +x ticlock-x86_64.AppImage

mkdir -v /runner/page/
cp -rv /source/* /runner/page/