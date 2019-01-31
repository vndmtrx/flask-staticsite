#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from flask import Flask, render_template, make_response, abort
from flask_staticsite import StaticSite

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
hdl = logging.StreamHandler()
#fmt = logging.Formatter('[%(asctime)s, %(name)s, %(funcName)s, %(lineno)s]: %(levelname)s - %(message)s')
fmt = logging.Formatter('[%(asctime)s - %(filename)s:%(lineno)s %(funcName)10s()]: %(levelname)s %(message)s')
hdl.setFormatter(fmt)
logger.addHandler(hdl)

import datetime
def dateslug(meta):
    parse_time='%Y-%m-%d %H:%M %z'
    format_time='%Y/%m'
    if isinstance(meta['date'], datetime.date):
        dt = meta['date']
    else:
        dt = datetime.datetime.strptime(meta['date'], parse_time)
    return '{0}/{1}'.format(dt.strftime(format_time), meta['slug'])

app = Flask(__name__)
app.config.from_pyfile('page.cfg')
site = StaticSite()
site.keymap_strategy = dateslug

posts_per_page = 3

@app.route('/')
def get_all_posts():
    lspages = site.sitemap.pagelist.sort('date')
    lstags = site.sitemap.header_values('tags')
    return render_template('index.html', pages=lspages, tags=lstags)

@app.route('/page/', defaults={'pag': 1})
@app.route('/page/<int:pag>')
def get_paginated_posts(pag):
    lspages = site.sitemap.pagelist.sort('date').paginate(posts_per_page)
    pp = lspages[pag-1]
    return render_template('paginate.html', ppages=pp, pag=pag, l=len(lspages))

@app.route('/tags/<tag>')
def get_tags(tag):
    lstags = site.sitemap.pagelist.filter('tags', tag)
    if len(lstags) > 0:
        return render_template('tags.html', tag=tag, tags=lstags)
    else:
        abort(404)

@app.route('/<path:slug>.html')
def get_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        return render_template('page.html', page=page)
    else:
        abort(404)

@app.route('/<path:slug>.txt')
def get_content_page(slug):
    if slug in site.sitemap.pages:
        page = site.sitemap.pages[slug]
        r = make_response(page.content)
        r.headers['Content-Type'] = 'text/plain; charset=utf-8'
        return r
    else:
        abort(404)

@app.route('/<path:slug>.raw')
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
