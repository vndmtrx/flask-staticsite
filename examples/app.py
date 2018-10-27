#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from flask import Flask, render_template, make_response, abort
from flask_staticsite import StaticSite

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
hdl = logging.StreamHandler()
#fmt = logging.Formatter('[%(asctime)s, %(name)s, %(funcName)s, %(lineno)s]: %(levelname)s - %(message)s')
fmt = logging.Formatter('[%(filename)s:%(lineno)s %(funcName)10s()]: %(levelname)s %(message)s')
hdl.setFormatter(fmt)
logger.addHandler(hdl)

app = Flask(__name__)
app.config.from_pyfile('page.cfg')
site = StaticSite()

@app.route('/')
def hello():
    user = {'username': 'Miguel'}
    return render_template('index.html', sitemap=site.sitemap)

@app.route('/<slug>.html')
def get_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        return render_template('page.html', page=page)
    else:
        abort(404)

@app.route('/<slug>.txt')
def xpage(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        r = make_response(page.content)
        r.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return r
    else:
        abort(404)

if __name__ == '__main__':
    site.init_app(app)
    app.run(debug=True)
