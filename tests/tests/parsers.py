from __future__ import with_statement
import os
from unittest2 import skipIf

try:
    import lxml
except ImportError:
    lxml = None

try:
    import html5lib
except ImportError:
    html5lib = None

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    BeautifulSoup = None


from django.conf import settings

from compressor.base import SOURCE_HUNK, SOURCE_FILE

from .base import CompressorTestCase


class ParserTestCase(object):

    def setUp(self):
        self.old_parser = settings.COMPRESS_PARSER
        settings.COMPRESS_PARSER = self.parser_cls
        super(ParserTestCase, self).setUp()

    def tearDown(self):
        settings.COMPRESS_PARSER = self.old_parser


class LxmlParserTests(ParserTestCase, CompressorTestCase):
    parser_cls = 'compressor.parser.LxmlParser'
LxmlParserTests = skipIf(lxml is None, 'lxml not found')(LxmlParserTests)


class Html5LibParserTests(ParserTestCase, CompressorTestCase):
    parser_cls = 'compressor.parser.Html5LibParser'

    def test_css_split(self):
        out = [
            (SOURCE_FILE, os.path.join(settings.COMPRESS_ROOT, u'css/one.css'), u'css/one.css', u'<link href="/media/css/one.css" rel="stylesheet" type="text/css">'),
            (SOURCE_HUNK, u'p { border:5px solid green;}', None, u'<style type="text/css">p { border:5px solid green;}</style>'),
            (SOURCE_FILE, os.path.join(settings.COMPRESS_ROOT, u'css/two.css'), u'css/two.css', u'<link href="/media/css/two.css" rel="stylesheet" type="text/css">'),
        ]
        split = self.css_node.split_contents()
        split = [(x[0], x[1], x[2], self.css_node.parser.elem_str(x[3])) for x in split]
        self.assertEqual(out, split)

    def test_js_split(self):
        out = [
            (SOURCE_FILE, os.path.join(settings.COMPRESS_ROOT, u'js/one.js'), u'js/one.js', u'<script src="/media/js/one.js" type="text/javascript"></script>'),
            (SOURCE_HUNK, u'obj.value = "value";', None, u'<script type="text/javascript">obj.value = "value";</script>'),
        ]
        split = self.js_node.split_contents()
        split = [(x[0], x[1], x[2], self.js_node.parser.elem_str(x[3])) for x in split]
        self.assertEqual(out, split)

Html5LibParserTests = skipIf(
    html5lib is None, 'html5lib not found')(Html5LibParserTests)


class BeautifulSoupParserTests(ParserTestCase, CompressorTestCase):
    parser_cls = 'compressor.parser.BeautifulSoupParser'

BeautifulSoupParserTests = skipIf(
    BeautifulSoup is None, 'BeautifulSoup not found')(BeautifulSoupParserTests)


class HtmlParserTests(ParserTestCase, CompressorTestCase):
    parser_cls = 'compressor.parser.HtmlParser'

