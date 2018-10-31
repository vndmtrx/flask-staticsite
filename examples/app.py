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
def get_all_posts():
    lspages = site.sitemap.pages.values()
    lstags = site.sitemap.header_values('tags')
    return render_template('index.html', pages=lspages, tags=lstags)

@app.route('/tags/<tag>')
def get_tags(tag):
    dttags = dict(site.sitemap.filter_by_header('tags', tag))
    return render_template('tags.html', tag=tag, tags=dttags.values())

@app.route('/<slug>.html')
def get_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        return render_template('page.html', page=page)
    else:
        abort(404)

@app.route('/<slug>.txt')
def get_content_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        r = make_response(page.content)
        r.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return r
    else:
        abort(404)

@app.route('/<slug>.raw')
def get_raw_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        r = make_response(page.raw)
        r.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return r
    else:
        abort(404)

if __name__ == '__main__':
    site.init_app(app)
    app.run(debug=True)
