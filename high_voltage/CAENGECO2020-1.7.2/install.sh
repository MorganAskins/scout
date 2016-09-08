#!/bin/sh

DEST_DIR="/usr/share/CAEN"
DEST_GECO_DIR="CAENGECO2020"
PLUGINS="plugins/imageformats"

WRAPPER="5.82"
VME="2.30.2"
COMM="1.02"
QT="4.7.4"
PHONON="4.2.0"
MANUAL="UM2463_GECO2020_REV9.pdf"

if [ `getconf LONG_BIT` = "64" ]
then
	echo "64 bit version detected"
	DEST_LIB_DIR="/usr/lib64"
	BIN_DIR="./bin/x64"
	LIB_DIR="./lib/x64"
	QT_DIR="./qt/x64"
	
	if [ ! -d $DEST_LIB_DIR ]; then
		DEST_LIB_DIR="/usr/lib"
	fi
else
	echo "32 bit version detected"
	DEST_LIB_DIR="/usr/lib"
	BIN_DIR="./bin"
	LIB_DIR="./lib"
	QT_DIR="./qt"
fi

DOC_DIR="./doc"

ERROR="Please ensure you have the rights to execute this command."

set -e

echo "Installing software..."

if ! [ $(id -u) = 0 ]; then
	echo
	echo "Unable to get root privileges."   
	echo $ERROR
	exit 1
fi

if [ -d $DEST_DIR/$DEST_GECO_DIR ]; then
	echo "Removing old version..."
	rm -rf $DEST_DIR/$DEST_GECO_DIR/* || { echo $ERROR ; exit 1; }
fi

echo "Creating directories..."

if [ ! -d $DEST_DIR/$DEST_GECO_DIR ]; then
	mkdir -p $DEST_DIR/$DEST_GECO_DIR || { echo $ERROR ; exit 1; }
fi

if [ ! -d $DEST_DIR/$DEST_GECO_DIR/$PLUGINS ]; then
	mkdir -p $DEST_DIR/$DEST_GECO_DIR/$PLUGINS || { echo $ERROR ; exit 1; }
fi

echo "Copying CAEN libraries..."
rm -f $DEST_LIB_DIR/libcaenhvwrapper.so || { echo $ERROR ; exit 1; }
cp -f $LIB_DIR/libcaenhvwrapper.so.$WRAPPER $DEST_LIB_DIR/libcaenhvwrapper.so.$WRAPPER || { echo $ERROR ; exit 1; }
chmod +r $DEST_LIB_DIR/libcaenhvwrapper.so.$WRAPPER || { echo $ERROR ; exit 1; }
ln -fs $DEST_LIB_DIR/libcaenhvwrapper.so.$WRAPPER $DEST_LIB_DIR/libcaenhvwrapper.so || { echo $ERROR ; exit 1; }

rm -f $DEST_LIB_DIR/libCAENVME.so || { echo $ERROR ; exit 1; }
cp -f $LIB_DIR/libCAENVME.so.$VME $DEST_LIB_DIR/libCAENVME.so.$VME || { echo $ERROR ; exit 1; }
chmod +r $DEST_LIB_DIR/libCAENVME.so.$VME || { echo $ERROR ; exit 1; }
ln -fs $DEST_LIB_DIR/libCAENVME.so.$VME $DEST_LIB_DIR/libCAENVME.so || { echo $ERROR ; exit 1; }

rm -f $DEST_LIB_DIR/libCAENComm.so || { echo $ERROR ; exit 1; }
cp -f $LIB_DIR/libCAENComm.so.$COMM $DEST_LIB_DIR/libCAENComm.so.$COMM || { echo $ERROR ; exit 1; }
chmod +r $DEST_LIB_DIR/libCAENComm.so.$COMM || { echo $ERROR ; exit 1; }
ln -fs $DEST_LIB_DIR/libCAENComm.so.$COMM $DEST_LIB_DIR/libCAENComm.so || { echo $ERROR ; exit 1; }

echo "Copying Qt libraries..."
if [ ! -f $DEST_LIB_DIR/libQtCore.so.$QT ]; then
	cp $QT_DIR/libQtCore.so.$QT $DEST_LIB_DIR/libQtCore.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtCore.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f $DEST_LIB_DIR/libQtGui.so.$QT ]; then
	cp $QT_DIR/libQtGui.so.$QT $DEST_LIB_DIR/libQtGui.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtGui.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f /usr/lib/libQtWebKit.so.$QT ]; then
	cp $QT_DIR/libQtWebKit.so.$QT $DEST_LIB_DIR/libQtWebKit.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtWebKit.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f /usr/lib/libQtDBus.so.$QT ]; then
	cp $QT_DIR/libQtDBus.so.$QT $DEST_LIB_DIR/libQtDBus.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtDBus.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f /usr/lib/libQtXml.so.$QT ]; then
	cp $QT_DIR/libQtXml.so.$QT $DEST_LIB_DIR/libQtXml.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtXml.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f /usr/lib/libQtNetwork.so.$QT ]; then
	cp $QT_DIR/libQtNetwork.so.$QT $DEST_LIB_DIR/libQtNetwork.so.$QT || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libQtNetwork.so.$QT || { echo $ERROR ; exit 1; }
fi

if [ ! -f /usr/lib/libphonon.so.$PHONON ]; then
	cp $QT_DIR/libphonon.so.$PHONON $DEST_LIB_DIR/libphonon.so.$PHONON || { echo $ERROR ; exit 1; }
	chmod +r $DEST_LIB_DIR/libphonon.so.$PHONON || { echo $ERROR ; exit 1; }
fi

cp -rf $QT_DIR/$PLUGINS/libqgif.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }
cp -rf $QT_DIR/$PLUGINS/libqico.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }
cp -rf $QT_DIR/$PLUGINS/libqjpeg.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }
cp -rf $QT_DIR/$PLUGINS/libqmng.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }
cp -rf $QT_DIR/$PLUGINS/libqsvg.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }
cp -rf $QT_DIR/$PLUGINS/libqtiff.so $DEST_DIR/$DEST_GECO_DIR/$PLUGINS/ || { echo $ERROR ; exit 1; }

echo "Copying files..."

cp -f ./CAENGECO2020_Readme.txt $DEST_DIR/$DEST_GECO_DIR/ || { echo $ERROR ; exit 1; }
cp -f ./CAENGECO2020_ReleaseNotes.txt $DEST_DIR/$DEST_GECO_DIR/ || { echo $ERROR ; exit 1; }
cp -f ./CAENGECO2020_License_Agreement.txt $DEST_DIR/$DEST_GECO_DIR/ || { echo $ERROR ; exit 1; }
chmod +r $DEST_DIR/$DEST_GECO_DIR/CAENGECO2020_*
cp -f $BIN_DIR/CAENGECO2020 $DEST_DIR/$DEST_GECO_DIR/ || { echo $ERROR ; exit 1; }
chmod +rx $DEST_DIR/$DEST_GECO_DIR/CAENGECO2020 || { echo $ERROR ; exit 1; }
ln -fs $DEST_DIR/$DEST_GECO_DIR/CAENGECO2020 /usr/local/bin/CAENGECO2020 || { echo $ERROR ; exit 1; }
cp -f $DOC_DIR/$MANUAL $DEST_DIR/$DEST_GECO_DIR/ || { echo $ERROR ; exit 1; }
chmod +r $DEST_DIR/$DEST_GECO_DIR/$MANUAL || { echo $ERROR ; exit 1; }

echo "Running post-installation triggers..."
ldconfig

echo "Installation completed."
