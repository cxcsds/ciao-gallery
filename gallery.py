#!/usr/bin/env python

"Create the CIAO gallery pages"

# pylint: disable=consider-using-with
# pylint: disable=import-outside-toplevel

import os

CIAO_VERSION = "4.16"

CWD = os.getcwd()
DATA_DIR = os.path.join(CWD, "data")
PNG_DIR = os.path.join(CWD, "pngs")
TEST_DIR = os.path.join(CWD, "tests/ciao_gallery")


def ch_data_dir(somefun):
    "decorator to change dir and back again"
    def wrapper(*args, **kwargs):
        "wrapper func"
        os.chdir(DATA_DIR)
        stt = somefun(*args, **kwargs)
        os.chdir(CWD)
        return stt
    return wrapper


class GalleryDoc():
    "Class to generate the gallery page"

    def writer(self, val):
        "Write output"
        self.outfile.write(val.strip()+"\n")

    def __init__(self, title, outfile):
        "Setup page"
        self.title = title
        self.outfile_name = outfile
        self.outfile = open(outfile, "w", encoding="ascii")
        self.examples = None
        self.__head()

    def __head(self):
        "Doc header"

        self.writer(f"""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
        <title><short>Gallery: {self.title}</short></title>

        <version>{CIAO_VERSION}</version>
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
        <div align='center'><h1>Gallery: {self.title}</h1></div>
        <p><cxclink href="thumbnail.html">Return to thumbnail page.</cxclink></p>
        """)

    def close(self):
        "Close page"
        self.__tail()
        self.outfile.close()

    def __tail(self):
        "Close xml"
        self.writer(" </text>\n</page>")

    def make_toc(self, examples):
        "Create the table of contents"
        self.examples = examples
        self.writer("""<h2>Examples</h2>
        <list type='1'>
        """)
        for i, e in enumerate(examples):
            e.num = i+1
            e.set_head()
            self.writer(f"""<li><cxclink id="{e.anchor}">{e.title}</cxclink></li>""")
        self.writer("""  </list>
        <hr/>""")

    def make_examples(self):
        "Create example"
        for exam in self.examples:
            for elm in ["hdr", "pre", "img", "cmd", "plt",  "pst"]:
                val = getattr(exam, elm)
                if val:
                    self.writer(val)
            self.writer("<hr/>")


class Thumbnail():
    "Class to create the thumbnail view"

    outfile = "thumbnail.xml"

    def writer(self, val):
        "Write page"
        self.fp.write(val.strip()+"\n")

    def __init__(self):
        "Setup"
        self.fp = open(self.outfile, "w", encoding="ascii")

        self.writer(f"""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
            <title><short>Thumbnails</short></title>

            <version>{CIAO_VERSION}</version>
            <css>div.section {{ clear: both; }}
                div.sectiontitle {{
                padding-top: 1em;
                text-align: center;
            }}
            div.example {{
                float: left;
                margin: 5px;
                padding: 10px;
                border-radius: 15px;
                background: #99cc66;
            }}
            </css>
        <breadcrumbs/>
        </info>
        <text>
        <div align='center'><h1>Thumbnails of CIAO examples</h1></div>
        <p><cxclink href="index.html">Go to list of gallery examples.</cxclink></p>
        <p>Select an image to see how it was created.</p>
        """)

    def add_section(self, gallery):
        "Create different sections"

        for gg in gallery:
            outf = gg.outfile_name.replace(".xml", ".html")
            self.writer(f"""<div class='section'>
            <div class='sectiontitle'>
              <h2><cxclink href='{outf}'>{gg.title}</cxclink></h2>
            </div>""")
            for ee in gg.examples:
                self.writer(f"""
                <div class='example'>
                  <div>{ee.title}</div>
                  <cxclink href='{outf}' id='{ee.anchor}'>
                    <img src='pngs/thmb.{ee.anchor}.png' alt='[{ee.title}]'/>
                  </cxclink>
                </div>
                """)
            self.writer("</div>")

    def close(self):
        "Close xml"
        self.writer(""" </text>
            </page>""")

        self.fp.close()


class IndexPage():
    "Class to create the index page"

    outfile = "index.xml"

    def writer(self, val):
        "Write outfile"
        self.fp.write(val.strip()+"\n")

    def __init__(self):
        "Setup"
        self.fp = open(self.outfile, "w", encoding="ascii")

        self.writer(f"""<?xml version='1.0' encoding='us-ascii' ?>
        <!DOCTYPE page>
        <!-- This page is automatically generated, do not edit -->
        <page>
        <info>
            <title><short>Gallery List</short></title>
            <version>{CIAO_VERSION}</version>
        <breadcrumbs/>
        </info>
        <text>
        <div align='center'><h1>List of CIAO examples</h1></div>
        <p><cxclink href="thumbnail.html">Go to thumbnail view.</cxclink></p>
        """)

    def add_section(self, gallery):
        "Add section"

        for gg in gallery:
            outf = gg.outfile_name.replace(".xml", ".html")
            self.writer(f"""<h2><cxclink href='{outf}'>{gg.title}</cxclink></h2>""")
            self.writer("<list>")
            for ee in gg.examples:
                self.writer(f"""<li><cxclink href='{outf}' id='{ee.anchor}'>{ee.title}</cxclink></li>""")
            self.writer("</list>")

    def close(self):
        "Close outfile"
        self.writer(""" </text>
            </page>""")

        self.fp.close()


def write_regression_tests(gallery):
    "Class to write commands to a regression test .MAIN file"

    for gg in gallery:
        for ee in gg.examples:
            with open(f"{TEST_DIR}/{ee.anchor}.MAIN", "w", encoding="ascii") as fp:
                for c in ee.raw_cmds:

                    for rr in ee.requires:
                        c = c.replace(rr, "${CT_INDIR}/"+rr)

                    fp.write(c+"\n")


class CIAOExample():
    "Class to hold parts of each example"

    def __init__(self, anchor, title):
        self.anchor = anchor
        self.title = title
        self.num = None
        self.hdr = None
        self.pre = None
        self.img = None
        self.cmd = None
        self.pst = None
        self.png = None
        self.plt = None
        self.raw_cmds = None
        self.requires = None
        print(f"Working on {self.anchor}")

    def set_head(self):
        "Print header line"
        self.hdr = f"""<h2><div id='{self.anchor}'/>{self.num}) {self.title}</h2>"""

    def set_pre(self, words_words_words):
        """This is the "pre" text; the text that appears describing
        the example"""

        self.pre = f"""<div class="before">{words_words_words}</div>"""

    def set_post(self, words_words_words):
        """This is the "post" test; the text that appears after the
        commands describing the commands"""
        self.pst = f"""<div class="after">{words_words_words}</div>"""

    @ch_data_dir
    def set_img(self, fits, extras, run=True):
        """This is the text to display the image"""

        self.img = f"""
        <cxclink href="pngs/{self.anchor}.png">
          <img class='chips' src='pngs/thmb.{self.anchor}.png' alt='{self.anchor}'/>
        </cxclink>"""

        import re
        nogeom = re.sub("-geometry *[0-9]*x[0-9]* ", "", extras)

        plt = f"ds9 {fits} {nogeom}"
        self.plt = f"""
            <div><p>The following commands can be used to visualize the output</p>
            <div class='examplecode'><screen>{plt}</screen></div>
            </div>"""

        if not run:
            return

        outf = os.path.join(PNG_DIR, self.anchor+".png")
        cmd = f"""ds9 {fits} -view info no -view colorbar yes -view magnifier no
        -view panner no -view buttons no -title foo -tile yes
        {extras} -saveimage {outf} -exit"""
        cmd = cmd.replace("\n", " ")
        print(cmd)
        if 0 != os.system(cmd):
            raise RuntimeError(f"problem making image {self.anchor}")

        if 0 != os.system(f"convert {PNG_DIR}/{self.anchor}.png -resize x320 {PNG_DIR}/thmb.{self.anchor}.png"):
            raise RuntimeError(f"problem making thumbnail for {self.anchor}")

    @ch_data_dir
    def set_cmds(self, cmds_to_run, run=False):
        """This is the text to run the commands"""

        self.raw_cmds = cmds_to_run

        for cc in cmds_to_run:
            if run and 0 != os.system(cc):
                raise RuntimeError(f"Problem running \n{cc}")

        ss = list(map(lambda x: x.strip(), cmds_to_run))
        for ii, cc in enumerate(ss):
            skip = ["pset", "punlearn", "pget", "ahelp"]
            for c0 in cc.split(" "):
                if c0 in skip:
                    continue
                if 0 == len(c0):
                    continue
                ciao = os.environ["ASCDS_INSTALL"]
                if os.path.exists(ciao+"/bin/"+c0) or os.path.exists(ciao+"/contrib/bin/"+c0):
                    cc = cc.replace(c0, f"""<ahelp name="{c0}"/>""")
                    skip.append(c0)
            ss[ii] = cc

        cmds = "\n".join(ss)
        self.cmd = f"""<div class='examplecode'><screen>{cmds}</screen></div>"""


def parse_cli():
    "Parse the command line options"

    import argparse

    cli_pars = argparse.ArgumentParser()
    cli_pars.add_argument("--infile", dest="infile", default="gallery.cfg",
                          action="store",
                          help="Configuration file name containing text and commands")
    cli_pars.add_argument("--skip-ds9", dest="run_ds9", default=True,
                          action="store_false", help="Skip running ds9 commands")
    cli_pars.add_argument("--skip-run", dest="run_cmd", default=True,
                          action="store_false", help="Skip running CIAO commands")

    args = cli_pars.parse_args()

    return args


def parse_config(options):
    "Parse the config file"

    import configparser as cfg
    tasks = cfg.ConfigParser()
    tasks.read_file(open(options.infile, "r", encoding="ascii"))

    pages = []
    examples = {}

    for task in tasks.sections():
        example = CIAOExample(task, tasks.get(task, "title"))
        example.set_cmds(tasks.get(task, "commands").strip().replace("\\\n", "").split("\n"),
                         run=options.run_cmd)
        example.set_img(tasks.get(task, "outfile"), tasks.get(task, "ds9_extras"),
                        run=options.run_ds9)
        if tasks.has_option(task, "pretext"):
            example.set_pre(tasks.get(task, "pretext"))
        if tasks.has_option(task, "posttext"):
            example.set_post(tasks.get(task, "posttext"))

        if tasks.has_option(task, "requires"):
            example.requires = tasks.get(task, "requires").strip().split()

        tt = task.split(".")[0]
        if tt not in pages:
            pages.append(tt)
            examples[tt] = [example]
        else:
            examples[tt].append(example)

    return pages, examples


def build_pages(pages, examples):
    "Create the pages"
    toc = []

    for page in pages:
        doc = GalleryDoc(page.capitalize(), page+".xml")
        doc.make_toc(examples[page])
        doc.make_examples()
        doc.close()
        toc.append(doc)

    tt = Thumbnail()
    tt.add_section(toc)
    tt.close()

    tt = IndexPage()
    tt.add_section(toc)
    tt.close()

    write_regression_tests(toc)


def main():
    "Main routine"
    options = parse_cli()
    pages, examples = parse_config(options)
    build_pages(pages, examples)


if __name__ == "__main__":
    main()
