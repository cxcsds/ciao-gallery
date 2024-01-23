#!/usr/bin/env python

import sys
import os

cwd=os.getcwd()
data_dir = os.path.join( cwd, "data")
png_dir = os.path.join( cwd, "pngs")
xml_dir = cwd
test_dir = os.path.join( cwd, "tests/ciao_gallery")


def ch_data_dir(somefun):
    def wrapper(*args, **kwargs ):
        os.chdir( data_dir )
        stt = somefun( *args, **kwargs )
        os.chdir( cwd )
        return(stt)
    return wrapper
    

class GalleryDoc(object):    

    def writer( self, val ):
        self.outfile.write( val.strip()+"\n")

    def __init__(self, title, outfile):
        self.title=title
        self.outfile_name = outfile
        self.outfile = open( outfile, "w")
        self.__head()        
        
    
    def __head(self):
        self.writer("""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
        <title><short>Gallery: {0}</short></title>
        
        <version>4.12</version>
        <css>img.chips {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        }}
        div.examplecode {{
        padding-left: 0.5em;
        background: #99CC66;
        }}
        div.hardcopies {{
        text-align: center;
        }}
        </css>
        <breadcrumbs/>
        </info>
        <text>
        <div align='center'><h1>Gallery: {0}</h1></div>
        <p><cxclink href="thumbnail.html">Return to thumbnail page.</cxclink></p>
        """.format(self.title))

    def close(self):
        self.__tail()
        self.outfile.close()
    
    def __tail(self):
        self.writer(" </text>\n</page>")
        
    def make_toc(self, examples):        
        self.examples = examples
        self.writer("""<h2>Examples</h2>
        <list type='1'>
        """)
        for i,e in enumerate(examples):
            e.num = i+1
            e.set_head()
            self.writer("""<li><cxclink id="{0}">{1}</cxclink></li>""".format(e.anchor, e.title))
        self.writer("""  </list>
        <hr/>""")

    def make_examples(self):
        for exam in self.examples:
            for elm in ["hdr", "pre", "img", "cmd", "plt",  "pst", "ftr"]:
                val = getattr( exam, elm )
                if val:
                    self.writer(val)
            self.writer("<hr/>")


class Thumbnail(object):

    def writer( self, val ):
        self.fp.write( val.strip()+"\n")
    
    def __init__(self):
        
        self.fp = open("thumbnail.xml","w")

        self.writer("""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
            <title><short>Thumbnails</short></title>
            
            <version>4.12</version>
            <css>div.section { clear: both; }
                div.sectiontitle {
                padding-top: 1em;
                text-align: center;
            }
            div.example {
                float: left;
                margin: 5px;
                padding: 10px;
                border-radius: 15px;
                background: #99cc66;
            }
            </css>
        <breadcrumbs/>
        </info>
        <text>
        <div align='center'><h1>Thumbnails of CIAO examples</h1></div>
        <p><cxclink href="index.html">Go to list of gallery examples.</cxclink></p>
        <p>Select an image to see how it was created.</p>
        """)

    def add_section(self, gallery):
        
        for gg in gallery:
            self.writer("""<div class='section'>
            <div class='sectiontitle'><h2><cxclink href='{}'>{}</cxclink></h2></div>""".format(gg.outfile_name.replace(".xml",".html"), gg.title))
            for ii,ee in enumerate(gg.examples):
                self.writer("""
                <div class='example'><div>{3}</div><cxclink href='{1}' id='{2}'><img src='pngs/thmb.{2}.png' alt='[{3}]'/></cxclink></div>
                """.format(ii+1, gg.outfile_name.replace(".xml",".html"), ee.anchor, ee.title ))
            self.writer("</div>")

    
    def close(self):
        
        self.writer(""" </text>
            </page>""")
        
        self.fp.close()
        


class IndexPage(object):

    def writer( self, val ):
        self.fp.write( val.strip()+"\n")
    
    def __init__(self):
        
        self.fp = open("index.xml","w")

        self.writer("""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
            <title><short>Gallery List</short></title>            
            <version>4.12</version>
        <breadcrumbs/>
        </info>
        <text>
        <div align='center'><h1>List of CIAO examples</h1></div>
        <p><cxclink href="thumbnail.html">Go to thumbnail view.</cxclink></p>
        """)

    def add_section(self, gallery):
        
        for gg in gallery:
            self.writer("""<h2><cxclink href='{}'>{}</cxclink></h2>""".format(gg.outfile_name.replace(".xml",".html"), gg.title))
            self.writer("<list>")
            for ii,ee in enumerate(gg.examples):
                self.writer("""
                <li><cxclink href='{1}' id='{2}'>{3}</cxclink></li>
                """.format(ii+1, gg.outfile_name.replace(".xml",".html"), ee.anchor, ee.title ))
            self.writer("</list>")

    
    def close(self):
        
        self.writer(""" </text>
            </page>""")
        
        self.fp.close()



class RegressionTest(object):
    
    def writer( self, val ):
        self.fp.write( val.strip()+"\n")

    def close( self ):
        self.fp.close()
    
    def __init__(self):
        pass
        
    def add_section(self, gallery):
        for gg in gallery:
            for ee in gg.examples:
                with open( "{}/{}.MAIN".format(test_dir, ee.anchor), "w") as fp:
                    for c in ee.raw_cmds:

                        for rr in ee.requires:
                            c = c.replace( rr, "${CT_INDIR}/"+rr)

                        fp.write(c+"\n")
                    


        
class CIAOExample( object ):    

    def __init__( self, anchor, title ):
        self.anchor=anchor
        self.title=title
        self.num = None
        print("Working on {}".format(self.anchor))

        self.hdr = None
        self.pre = None
        self.img = None
        self.cmd = None
        self.pst = None
        self.ftr = None
        self.png = None
        self.plt = None

    def set_head( self ):
        self.hdr = """<h2><div id='{0}'/>{1}) {2}</h2>""".format( self.anchor, self.num, self.title )

    def __tail( self ):
        self.ftr = ""

    def set_pre( self, words_words_words ):
        self.pre="""<div class="before">{0}</div>""".format(words_words_words)
        
    def set_post( self, words_words_words ):
        self.pst="""<div class="after">{0}</div>""".format(words_words_words)
    
    @ch_data_dir
    def set_img(self,fits, extras, run=True):

        #print "ds9 -title foo {1} {0} -saveimage {2} -exit".format(extras, fits, self.anchor+".png")
        self.img = """<cxclink href="pngs/{0}.png"><img class='chips' src='pngs/thmb.{0}.png' alt='{0}'/></cxclink>""".format(self.anchor)


        import re
        nogeom = re.sub("-geometry *[0-9]*x[0-9]* ", "", extras)

        plt = "ds9 {infiles} {xtra}".format( xtra=nogeom, infiles=fits )
        self.plt = """
            <div><p>The following commands can be used to visualize the output</p>
            <div class='examplecode'><screen>{0}</screen></div>
            </div>""".format( plt )

        if not run:
            return

        cmd = """ds9 {infiles} -view info no -view colorbar yes -view magnifier no 
        -view panner no -view buttons no -title foo -tile yes
        {xtra} -saveimage {outfile} -exit""".format(xtra=extras, infiles=fits, outfile=os.path.join( png_dir, self.anchor+".png"))
        cmd = cmd.replace("\n"," ")
        print(cmd)
        if 0 != os.system(cmd):
            raise RuntimeError( "problem making image {}".format(self.anchor))
        
        if 0 != os.system("convert {1}/{0}.png -resize x320 {1}/thmb.{0}.png".format(self.anchor,png_dir)):
            raise RuntimeError("problem making thumbnail for {0}".format(self.anchor))


    @ch_data_dir
    def set_cmds(self, cmds_to_run, run=False):
        
        self.raw_cmds = cmds_to_run
        
        for cc in cmds_to_run:
            if run and 0 != os.system( cc ):
                raise RuntimeError("Problem running \n{}".format(cc))

        ss = list(map(lambda x: x.strip(), cmds_to_run))
        for ii,cc in enumerate(ss):
            #c0 = cc.split(" ")[0]
            skip = [ "pset", "punlearn", "pget", "ahelp"]
            for c0 in cc.split(" "):
                if c0 in skip: 
                    continue
                if 0 == len(c0):
                    continue
                ciao = os.environ["ASCDS_INSTALL"]
                if os.path.exists( ciao+"/bin/"+c0 ) or os.path.exists( ciao+"/contrib/bin/"+c0):
                    cc=cc.replace( c0, """<ahelp name="{}"/>""".format(c0))
                    skip.append(c0)
            ss[ii] = cc


        self.cmd = """<div class='examplecode'><screen>{0}</screen></div>""".format( "\n".join(ss) )
        

#--------------------------------------------------


#import ConfigParser as cfg
import configparser as cfg
tasks = cfg.ConfigParser()
tasks.readfp( open( "gallery.cfg", "r"))

pages = []
examples = {}

for task in tasks.sections():
    example = CIAOExample( task, tasks.get(task,"title"))
    example.set_cmds( tasks.get(task,"commands").strip().replace("\\\n","").split("\n"), run=tasks.getboolean(task,"run_cmd") )
    example.set_img( tasks.get(task,"outfile"), tasks.get(task, "ds9_extras"), run=tasks.getboolean(task,"run_ds9"))
    if tasks.has_option(task,"pretext") : 
        example.set_pre( tasks.get(task,"pretext"))
    if tasks.has_option(task,"posttext") : 
        example.set_post( tasks.get(task,"posttext"))

    if tasks.has_option(task, "requires"):
        example.requires = tasks.get(task,"requires").strip().split()
    else:
        example.requires = None


    tt = task.split(".")[0] 
    if tt not in pages: 
        pages.append( tt )
        examples[tt] = [ example ]
    else:
        examples[tt].append( example )


toc = []

for page in pages:
    doc = GalleryDoc( page.capitalize(), page+".xml" )
    doc.make_toc( examples[page] )
    doc.make_examples()
    doc.close()
    toc.append( doc )



tt = Thumbnail()
tt.add_section( toc )
tt.close()


tt = IndexPage()
tt.add_section( toc )
tt.close()

zz = RegressionTest()
zz.add_section(toc)

