REM_HOST=86.107.98.200
rsync -urltv -e ssh --delete --copy-links ~/lav/src/spiega/markdown/ $REM_HOST:~/webdav/
#unison ~/lav/src/spiega/markdown/ $REM_HOST:~/webdav/
#rclone

