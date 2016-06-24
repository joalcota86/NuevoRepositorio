#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, time, urllib2
from urllib import urlopen

def verify():
    url='https://theproxylist.eu/kickass.html'
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    
    list_urls=re.compile('<tr>\n<td>.+?</td>\n<td><a href="(.+?)">.+?</a></td>\n<td>.+?</td>\n<td><img src=".+?"></td>\n</tr>').findall(link)
    
    print "POSIBLES: " + str(list_urls)
    
    
    verified = []
    
    
    
    for this_url in list_urls :
        try:
            response=urllib2.urlopen(this_url,timeout=3)
            link=response.read()
            match=re.compile('KickassTorrents').findall(link)
            if match[0] == "KickassTorrents":
                verified.append(this_url)
                print ". " + this_url + " ... YES"
            else:
                print ". " + this_url + " ... NO MATCH"
        except:
            print ". " + this_url + " ... NO"
    
    print "OK: " + str(verified)
    
    return verified[0]


