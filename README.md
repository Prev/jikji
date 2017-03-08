# Jikji
[![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi)
[![Build Status](https://travis-ci.org/Prev/jikji.svg?branch=master)](https://travis-ci.org/Prev/jikji)  

Static website generator adapting View-ViewModel Pattern 



## What's different
In common static website generator like [Jekyll](https://jekyllrb.com/),   it transform **plain text** like mardown to html.

Jekyll is blog-friendly generator, but `jikji` is general-purpose static website generator communicate with **DBMS** or **RESTFul API Server**.


## Install
```bash
$ pip install jikji
```


## Usage
```bash
$ jikji <my_site> generate
```


## Open server for testing
You don't have to generate all the time after modify template.  
`Jikji` has useful function to develop in realtime

Run jikji as __listening__ mode

```bash
$ jikji <my_site> listen
$ jikji <my_site> listen --port PORT --host HOST
```

Then you can see rendered website in your browser (default: http://localhost:7000)

Web server opened with [Flask](http://flask.pocoo.org/), and when you reload the website, jikji will re-rendering template.


## template engine
`jikji` use [Jinja2](http://jinja.pocoo.org) template engine which is used in [Flask](http://flask.pocoo.org/).  
You can see jinja template documentation on [here](http://jinja.pocoo.org/docs/dev/templates/).

  


