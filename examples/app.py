#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import Flask, abort
from flask_staticsite import StaticSite

app = Flask(__name__)
app.config.from_pyfile('page.cfg')
site = StaticSite()
site.init_app(app)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<slug>')
def page(slug):
    print(slug)
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        return page.content
    else:
        abort(404)

if __name__ == '__main__':
    app.run()
