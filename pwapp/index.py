import json
import urllib
import os
import sys
import sqlite3
import hashlib
import datetime
import random
import pwapp
import time
import yaml
from unidecode import unidecode
import requests
import urllib3
import xmltodict
import pickle
from itertools import combinations
import re
import html
import subprocess
import urllib.parse
urllib3.disable_warnings()

def sanitize_value(value: str) -> str:
    value = value.strip()
    return re.sub(r'[^\w\s,-]', '', value)
    
class TableClass():

    def return_string(self, cont):
        return cont.encode("utf-8")

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response
        self.get_done = "Get done."
        self.string_remove = "Remove done."
        self.string_put = "Save done."
        self.string_insert = "Save done."
        self.string_save = "Save done."
        self.string_key_conflict = "Key conflict."
        self.pars = self.parse_fields(self.environ)
        self.db = {}

    def __iter__(self):
        status = '200 OK'
        response_type = self.pars.get("response_type", None)
        if response_type in ["plain", None]:
            response_headers = [('Content-type','text/plain; charset=utf-8')]
        elif response_type in ["json"]:
            response_headers = [('Content-type','application/json; charset=utf-8')]
        else:
            response_headers = [('Content-type','text/plain; charset=utf-8')]
        self.stream_out = self.start(status, response_headers)

        try:
            method = getattr(self, sanitize_value(self.pars.get("action", "version")))
            yield from method()
        except AttributeError:
            yield from self.error("method not found")

    def parse_fields(self, environ):
        method = environ.get("REQUEST_METHOD", "").upper()
        pars = {}

        if method == "GET":
            qs = environ.get("QUERY_STRING", "")
            parsed = urllib.parse.parse_qs(qs, keep_blank_values=True)
            # flatten values (same behavior as your code)
            pars = {k: v[0] for k, v in parsed.items()}

        elif method == "POST":
            content_type = environ.get("CONTENT_TYPE", "")
            content_length = int(environ.get("CONTENT_LENGTH", 0))

            body = environ["wsgi.input"].read(content_length)

            if content_type.startswith("application/x-www-form-urlencoded"):
                parsed = urllib.parse.parse_qs(
                    body.decode("utf-8"),
                    keep_blank_values=True
                )
                pars = {k: v[0] for k, v in parsed.items()}

            elif content_type.startswith("application/json"):
                pars = json.loads(body.decode("utf-8"))

            else:
                raise ValueError(f"Unsupported Content-Type: {content_type}")

        return pars

    def version(self):
        status_string = f"""pwapp v1 {datetime.datetime.now()}"""
        return [self.return_string(status_string)]

    def echo(self):
        message = self.pars.get("message", "no_message")
        return [self.return_string(message)]

def application(environ, start_response):
    return iter(TableClass(environ, start_response))
