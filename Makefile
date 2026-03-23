
CIAOVER = 418


index.xml: gallery.cfg gallery.py
	python gallery.py
	/bin/ls *.xml pngs/*png | cpio -pdv --quiet /data/da/Docs/ciaoweb/ciao$(CIAOVER)/gallery/ |& grep -E -v "newer"
	(cd /data/da/Docs/ciaoweb/ciao$(CIAOVER)/gallery/ ; perl /data/da/Docs/web4/ciao$(CIAOVER)/publish_all.pl -y |& grep -E -v skip)
