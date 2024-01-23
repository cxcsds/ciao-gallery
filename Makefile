index.xml: gallery.cfg gallery.py
	python gallery.py
	/bin/ls *.xml pngs/*png | cpio -pdv --quiet /data/da/Docs/ciaoweb/ciao416/gallery/ |& egrep -v "newer"
	(cd /data/da/Docs/ciaoweb/ciao416/gallery/ ; perl /data/da/Docs/web4/ciao416/publish_all.pl -y |& egrep -v skip)   
