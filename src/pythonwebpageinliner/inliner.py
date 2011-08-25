#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim:tabstop=4:expandtab:sw=4:softtabstop=4

# TODO
#   do smart image translation, CSS' often declare background and
#   background-image urls check python-cssutils, if it's of any use. for now
#   it's a naive regexp

import argparse
import base64
import feedparser  # feedparser has a _kick ass_ charset detection function!
import mimetypes
import re
import sys
import urllib2

from BeautifulSoup import BeautifulSoup
from itertools import chain
from urlparse import urljoin
from urlparse import urlparse


URL_BLACKLIST = ('getsatisfaction.com',
                 'google-analytics.com',
                )
CSS_URL = re.compile(ur'url\((.+)\)')


def parse_args():
    """Parse the args using argparse library"""
    desc = "Fetch a url and inline the external elements such as CSS/JS/Images"

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('-u', '--url', dest='url',
                            action='store',
                            default=None,
                            required=True,
                            help='the url to fetch content from')

    parser.add_argument('-o', '--output', dest='output',
                            action='store',
                            default='result.html',
                            required=False,
                            help='the output file, if not specified result.html is used')

    args = parser.parse_args()
    return args


def is_remote(address):
    """Checking for http/https in the url"""
    return urlparse(address)[0] in ('http', 'https')


def data_encode_image(name, content):
    """Construct the data uri with mime type and base64ing

    Example format:
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA
        AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO
        9TXL0Y4OHwAAAABJRU5ErkJggg==" alt="Red dot">

    """
    return u'data:{0};base64,{1}'.format(
                mimetypes.guess_type(name)[0],
                base64.standard_b64encode(content))


def ignore_url(address):
    """Ignore known tracking/analytics urls"""

    for bli in URL_BLACKLIST:
        if address.find(bli) != -1:
            return True

    return False


def get_content(from_, expect_binary=False):
#{{
    if is_remote(from_):
        if ignore_url(from_):
            return u''

        ct = urllib2.urlopen(from_)
        if not expect_binary:
            s = ct.read()
            encodings = feedparser._getCharacterEncoding(ct.headers, s)
            return unicode(s, encodings[0])
        else:
            return ct.read()
    else:
        s = open(from_).read()
        if not expect_binary:
            encodings = feedparser._getCharacterEncoding({}, s)
            return unicode(s, encodings[0])
        else:
            return s
#}}


def resolve_path(base, target):
#{{
    if True:
        return urljoin(base, target)

    if is_remote(target):
        return target

    if target.startswith('/'):
        if is_remote(base):
            protocol, rest = base.split('://')
            return '%s://%s%s' % (protocol, rest.split('/')[0], target)
        else:
            return target
    else:
        try:
            base, rest = base.rsplit('/', 1)
            return '%s/%s' % (base, target)
        except ValueError:
            return target
#}}


def replaceJavascript(base_url, soup):
#{{
    for js in soup.findAll('script', {'src': re.compile('.+')}):
        try:
            real_js = get_content(resolve_path(base_url, js['src']))
            js.replaceWith(u'<script>%s</script>' % real_js)
        except Exception, exc:
            print 'failed to load javascript from %s' % js['src']
            print exc
            #js.replaceWith('<!-- failed to load javascript from %s -->' % js['src'])
#}}


def replaceCss(base_url, soup):
#{{
    for css in soup.findAll('link',
                            {
                                'rel': 'stylesheet',
                                'href': re.compile('.+')
                            }):
        try:
            real_css = get_content(resolve_path(base_url, css['href']))

            def replacer(result):
                try:
                    path = resolve_path(resolve_path(base_url,
                                                     css['href']),
                                                     result.groups()[0])

                    return u'url(%s)' % data_encode_image(path,
                                                          get_content(path,
                                                                      True))
                except Exception, exc:
                    print exc
                    return u''

            css.replaceWith(u'<style>%s</style>' % re.sub(CSS_URL,
                                                          replacer,
                                                          real_css))

        except Exception, exc:
            print 'failed to load css from %s' % css['href']
            print exc
            #css.replaceWith('<!-- failed to load css from %s -->' % css['href'])
#}}


def replaceImages(base_url, soup):
#{{
    for img in chain(soup.findAll('img', {'src': re.compile('.+')}),
                     soup.findAll('input',
                                  {'type': 'image', 'src': re.compile('.+')})):
        try:
            path = resolve_path(base_url, img['src'])
            real_img = get_content(path, True)
            img['src'] = data_encode_image(path.lower(), real_img)
        except Exception, exc:
            print 'failed to load image from %s' % img['src']
            print exc
            #img.replaceWith('<!-- failed to load image from %s -->' % img['src'])

#}}


def main():
    args = parse_args()

    bs = BeautifulSoup(get_content(args.url))

    replaceJavascript(args.url, bs)
    replaceCss(args.url, bs)
    replaceImages(args.url, bs)

    res = open(args.output, 'wb')
    print >> res, str(bs)
    res.close()

if __name__ == '__main__':
    main()
