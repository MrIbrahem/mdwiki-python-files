#!/usr/bin/python3
"""
# ---
from apis import open_url
# open_url.getURL(url)
# open_url.open_json_url(url)
# ---
"""
#
# (C) Ibrahem Qasim, 2023
#
import traceback
import json
import time
import requests
import sys

# ---
from newapi import printe
import pywikibot

# ---


class classgetURL:
    def __init__(self, url):
        self.start = time.time()
        self.url = url
        self.html = ''

    def open_it(self):
        if not self.url:
            printe.output('open_url.py: self.url == ""')
            return ''
        if 'printurl' in sys.argv:
            printe.output(f'getURL: {self.url}')

        try:
            # req = comms.http.fetch(self.url)
            req = requests.get(self.url, timeout=10)
            # ---
            if 500 <= req.status_code < 600:
                printe.output(f'received {req.status_code} status from {req.url}')
                self.html = ''
            else:
                # ---
                self.html = req.text
        # ---
        except Exception:
            _Except_ions_ = [
                "Too long GET request",
                "HTTPSConnectionPool(host='en.wikipedia.org', port=443): Read timed out. (read timeout=45)",
                "('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))",
                '''('Connection aborted.', OSError("(104, 'ECONNRESET')"))''',
                '''HTTP Error 414: URI Too Long''',
                "HTTP Error 500: Internal Server Error",
            ]
            pywikibot.output('<<red>> Traceback (most recent call last):')
            pywikibot.output(traceback.format_exc())
            pywikibot.output('CRITICAL:')
        # ---
        return self.html


def getURL(url, maxsleeps=0):
    bot = classgetURL(url)
    return bot.open_it()


def open_json_url(url, maxsleeps=0, **kwargs):
    bot = classgetURL(url)
    js_text = bot.open_it()
    # ---
    if '<!DOCTYPE html>' in js_text or '<!doctype html>' in js_text:
        printe.output(f'<<red>> open_json_url: url: {url} returns <!DOCTYPE html>!!')
        return {}
    # ---
    try:
        return json.loads(js_text)
    except json.JSONDecodeError:
        pywikibot.output(traceback.format_exc())
        printe.output(js_text)
        pywikibot.output(" CRITICAL:")
    except Exception:
        pywikibot.output(traceback.format_exc())
        printe.output(js_text)
        pywikibot.output(" CRITICAL:")
        return {}
