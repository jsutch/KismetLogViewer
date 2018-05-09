## Kismet Log Viewer
# Contributor: j0nk0
pkgname=kismetlogviewer
pkgver=3.1
pkgrel=1
pkgdesc="Combines multiple Kismet log files in the .netxml format, summarizes the data, and outputs an easy-to-read html or csv file"
url="https://github.com/j0nk0/KismetLogViewer/"
execname="klv"

build(){
	cd $(dirname $0)/

	# Kismet Log Viewer 3.1
	# https://github.com/j0nk0/KismetLogViewer/
	echo "Executables will be 'klv'..."
	mkdir -p /usr/share/klv
	install -m 755 -D $execname /usr/share/klv
	install -m 755 -D README.md /usr/share/klv
	install -m 644 -D oui.txt /usr/share/klv
	rm /usr/bin/klv
	ln -s /usr/share/klv/klv /usr/bin/klv
}
 build
