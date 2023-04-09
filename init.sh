#!/bin/sh

cp /etc/ssl/certs/ca-certificates.crt /

apk add --no-cache markdown
cd /source

echo '<!DOCTYPE html>' > index.html
echo '<html lang="en-US">' >> index.html
cat docs/head.html >> index.html

echo '<body>' >> index.html
markdown README.md >> index.html
echo '</body>' >> index.html
echo '</html>' >> index.html

apk add --no-cache py-pip linux-headers build-base python3-dev xvfb appstream tar libc6-compat

cp /ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
rm -f /etc/ssl/cert.pem
ln -s /etc/ssl/certs/ca-certificates.crt /etc/ssl/cert.pem

# FIX CERTIFICATES
for X in $(find /usr -name *.pem); do
    rm -f "$X"
    ln -s /etc/ssl/cert.pem "$X"
done

GLIBC_REPO=https://github.com/sgerrand/alpine-pkg-glibc
GLIBC_VERSION=2.30-r0

for pkg in glibc-${GLIBC_VERSION} glibc-bin-${GLIBC_VERSION}; \
    do curl -sSL ${GLIBC_REPO}/releases/download/${GLIBC_VERSION}/${pkg}.apk -o /tmp/${pkg}.apk
done

apk add --allow-untrusted --no-cache -f /tmp/*.apk
/usr/glibc-compat/sbin/ldconfig /lib /usr/glibc-compat/lib

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

for X in $(find . -name '__pycache__'); do
    rm -rf "$X"
done

DISPLAY=":0" pyinstaller -F --onefile --console \
 --additional-hooks-dir=. --add-data config.py:config.py --add-data modules/*:modules/ --add-data apps/*:apps/ \
  $py_deps_ticlock --add-data log/*:log/ -i docs/icon.png -n ticlock -c main.py

mv dist/ticlock .
rm -rf dist build log
strip ticlock

chmod +x ticlock

wget https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/x86_64/apk-tools-static-2.12.10-r1.apk -O installer.apk

cd /
tar -xzf /source/installer.apk
cd /source

rm -f installer.apk
/sbin/apk.static -X https://dl-cdn.alpinelinux.org/alpine/latest-stable/main -U --allow-untrusted -p /source/ticlock.AppDir/ --initdb add --no-cache alpine-base busybox libc6-compat

rm -rf ticlock.AppDir/{etc,var,home,mnt,srv,proc,sys,boot,opt}

cp docs/icon.png ticlock.AppDir/icon.png

echo '[Desktop Entry]' > ticlock.AppDir/ticlock.desktop
echo 'Name=ticlock' >> ticlock.AppDir/ticlock.desktop
echo 'Categories=Settings' >> ticlock.AppDir/ticlock.desktop
echo 'Type=Application' >> ticlock.AppDir/ticlock.desktop
echo 'Icon=icon' >> ticlock.AppDir/ticlock.desktop
echo 'Terminal=true' >> ticlock.AppDir/ticlock.desktop
echo 'Exec=/lib/ld-musl-x86_64.so.1 /usr/bin/ticlock' >> ticlock.AppDir/ticlock.desktop

chmod +x ticlock.AppDir/ticlock.desktop

echo '#!/bin/sh' > ticlock.AppDir/AppRun
echo 'TICLOCK_RUNPATH="$(dirname "$(readlink -f "${0}")")"' >> ticlock.AppDir/AppRun
echo 'TICLOCK_EXEC="${TICLOCK_RUNPATH}"/usr/bin/ticlock' >> ticlock.AppDir/AppRun
echo 'export LD_LIBRARY_PATH="${TICLOCK_RUNPATH}"/lib:"${TICLOCK_RUNPATH}"/lib64:$LD_LIBRARY_PATH' >> ticlock.AppDir/AppRun
echo 'export LIBRARY_PATH="${TICLOCK_RUNPATH}"/lib:"${TICLOCK_RUNPATH}"/lib64:"${TICLOCK_RUNPATH}"/usr/lib:"${TICLOCK_RUNPATH}"/usr/lib64:$LIBRARY_PATH' >> ticlock.AppDir/AppRun
echo 'export PATH="${TICLOCK_RUNPATH}/usr/bin/:${TICLOCK_RUNPATH}/usr/sbin/:${TICLOCK_RUNPATH}/usr/games/:${TICLOCK_RUNPATH}/bin/:${TICLOCK_RUNPATH}/sbin/${PATH:+:$PATH}"' >> ticlock.AppDir/AppRun
echo 'exec "${TICLOCK_RUNPATH}"/lib/ld-musl-x86_64.so.1 "${TICLOCK_EXEC}" "$@"' >> ticlock.AppDir/AppRun

chmod +x ticlock.AppDir/AppRun

mkdir -p ticlock.AppDir/usr/bin
cp ticlock ticlock.AppDir/usr/bin/
chmod +x ticlock.AppDir/usr/bin/ticlock

wget https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage -O toolkit.AppImage
chmod +x toolkit.AppImage

cd /opt/
/source/toolkit.AppImage --appimage-extract
mv /opt/squashfs-root /opt/appimagetool.AppDir
ln -s /opt/appimagetool.AppDir/AppRun /usr/local/bin/appimagetool
chmod +x /opt/appimagetool.AppDir/AppRun
cd /source

ARCH=x86_64 appimagetool ticlock.AppDir/

rm -rf ticlock.AppDir
rm -f toolkit.AppImage
chmod +x ticlock-x86_64.AppImage

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/