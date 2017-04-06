# Jikji
[![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi/jikji)
[![Build Status](https://travis-ci.org/Prev/jikji.svg?branch=2.0)](https://travis-ci.org/Prev/jikji)  
[![Python Versions](https://img.shields.io/pypi/pyversions/jikji.svg)](https://pypi.python.org/pypi/jikji)

Static website generator adapting View-Page Pattern 



## What's different
In common static website generator like [Jekyll](https://jekyllrb.com/),   it transforms **plain text** like mardown to html.

Jekyll is blog-friendly generator, but `Jikji` is general-purpose static website generator that communicates with **DBMS** or **RESTFul API Server**.


## Install
```bash
$ pip install jikji
```


## Usage
```bash
$ jikji <my_site> generate
```


## Open server for testing
You don't have to generate all the time after modifying template.  
`Jikji` has useful function to develop in realtime

Run jikji as __listening__ mode

```bash
$ jikji <my_site> listen
$ jikji <my_site> listen --port PORT --host HOST
```

Then you can see rendered website in your browser (default: http://localhost:7000)

When you reload the website running with [Flask](http://flask.pocoo.org/), jikji will do re-rendering the template.


## Template engine
`Jikji` uses [Jinja2](http://jinja.pocoo.org) template engine which is used in [Flask](http://flask.pocoo.org/).  
You can see jinja template documentation on [here](http://jinja.pocoo.org/docs/dev/templates/).

  


