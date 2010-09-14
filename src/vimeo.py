#!/usr/bin/env python

import re
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

class Vimeo(object):
    browser = mechanize.Browser()
    cookies = cookielib.LWPCookieJar()
    res = None
    html = None

    def __init__(self):
        self.browser.set_handle_robots(False)
        self.browser.set_cookiejar(self.cookies)
        self.browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def getToken(self):
        #input type="hidden" id="xsrft" class="xsrft" name="token" value="eb0fe03ceac5796bdde1ee2c8c9166cd"
        tokenRe = re.compile('<input type="hidden" id="xsrft" class="xsrft" name="token" value="(.*)"')
        m = tokenRe.search(self.html)
        if m:
            return m.group(1)
        else:
            raise Error()
        #soup = BeautifulSoup(self.html)
        #return soup.find('input', {'name':'token'})['value']

    def addCookieCheck(self, token):
        ck = cookielib.Cookie(version=0, name='xsrft', value=token, port=None, port_specified=False, domain='.vimeo.com', domain_specified=True, domain_initial_dot=True, path='/', path_specified=True, secure=False, expires=1599860849, discard=False, comment=None, comment_url=None, rest={}, rfc2109=False)
        self.cookies.set_cookie(ck)

    def goto(self, url):
        self.res = self.browser.open(url)
        self.html = self.res.read()

    def submit(self):
        self.res = self.browser.submit()
        self.html = self.res.read()

    def login(self, username, password):
        br = self.browser
        self.goto('http://vimeo.com/log_in')
        token = self.getToken()
        self.addCookieCheck(token)

        br.select_form(nr=0)
        br['sign_in[email]'] = username
        br['sign_in[password]'] = password
        tc = mechanize.TextControl('hidden', 'token', {'value':token})
        tc.add_to_form(br.form)
        self.submit()

    def upload(self, filename):
        self.goto('http://www.vimeo.com/upload/video')
        br = self.browser
        br.select_form(nr=1)
        tc = mechanize.TextControl('hidden', 'token', {'value':self.getToken()})
        tc.add_to_form(br.form)
        br.form.add_file(open(filename), 'application/octet-stream', filename)
        self.submit()

def main():
    v = Vimeo()
    v.login('username', 'password')
    v.upload('a_video_file')

if __name__ == "__main__":
    main()
