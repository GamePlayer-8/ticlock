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

apt install --yes python3-pip linux-headers-5.19.0-38-generic build-essential python3-dev xvfb appstream tar lsb-release apt-utils

pip install --upgrade wheel setuptools
pip install -r requirements.txt
pip install pyinstaller

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

mkdir -p ticlock.AppDir/var/lib/dpkg
mkdir -p ticlock.AppDir/var/cache/apt/archives
apt install --yes debootstrap fakeroot fakechroot
fakechroot fakeroot debootstrap --variant=fakechroot --arch amd64 $(lsb-release -sr) /source/ticlock.AppDir/ http://archive.ubuntu.com/ubuntu

rm -rf ticlock.AppDir/{etc,var,home,mnt,srv,proc,sys,boot,opt}

cp docs/icon.png ticlock.AppDir/icon.png

echo '[Desktop Entry]' > ticlock.AppDir/ticlock.desktop
echo 'Name=ticlock' >> ticlock.AppDir/ticlock.desktop
echo 'Categories=Settings' >> ticlock.AppDir/ticlock.desktop
echo 'Type=Application' >> ticlock.AppDir/ticlock.desktop
echo 'Icon=icon' >> ticlock.AppDir/ticlock.desktop
echo 'Terminal=true' >> ticlock.AppDir/ticlock.desktop
echo 'Exec=/usr/bin/ticlock' >> ticlock.AppDir/ticlock.desktop

chmod +x ticlock.AppDir/ticlock.desktop

echo '#!/bin/sh' > ticlock.AppDir/AppRun
echo 'TICLOCK_RUNPATH="$(dirname "$(readlink -f "${0}")")"' >> ticlock.AppDir/AppRun
echo 'TICLOCK_EXEC="${TICLOCK_RUNPATH}"/usr/bin/ticlock' >> ticlock.AppDir/AppRun
echo 'export LD_LIBRARY_PATH="${TICLOCK_RUNPATH}"/lib:"${TICLOCK_RUNPATH}"/lib64:$LD_LIBRARY_PATH' >> ticlock.AppDir/AppRun
echo 'export LIBRARY_PATH="${TICLOCK_RUNPATH}"/lib:"${TICLOCK_RUNPATH}"/lib64:"${TICLOCK_RUNPATH}"/usr/lib:"${TICLOCK_RUNPATH}"/usr/lib64:$LIBRARY_PATH' >> ticlock.AppDir/AppRun
echo 'export PATH="${TICLOCK_RUNPATH}/usr/bin/:${TICLOCK_RUNPATH}/usr/sbin/:${TICLOCK_RUNPATH}/usr/games/:${TICLOCK_RUNPATH}/bin/:${TICLOCK_RUNPATH}/sbin/${PATH:+:$PATH}"' >> ticlock.AppDir/AppRun
echo 'exec "${TICLOCK_EXEC}" "$@"' >> ticlock.AppDir/AppRun

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

mv ticlock ticlock-glibc
mv ticlock-x86_64.AppImage ticlock-glibc-x86_64.AppImage

rm -rf ticlock.AppDir
rm -f toolkit.AppImage
chmod +x ticlock-x86_64.AppImage

mkdir -pv /runner/page/
cp -rv /source/* /runner/page/