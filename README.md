# Jikji
[![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi/jikji)
[![Python Versions](https://img.shields.io/pypi/pyversions/jikji.svg)](https://pypi.python.org/pypi/jikji)
[![Build Status](https://travis-ci.org/Prev/jikji.svg)](https://travis-ci.org/Prev/jikji) 

Python Static website generator for Modern web


## What's different
Like the common static website generator, [Jekyll](https://jekyllrb.com/),   it transforms **plain text**, like mardown, to HTML.

Jekyll is a blog-friendly generator, but `Jikji` is the general-purpose static website generator that communicates with **DBMS** or **RESTFul API Server**.


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
`Jikji` has useful functions to develop in realtime.

Run jikji as __listening__ mode

```bash
$ jikji <my_site> listen
$ jikji <my_site> listen --port PORT --host HOST
```

Then you can see rendered website in your browser (default: http://localhost:7000)

When you reload the website running with [Flask](http://flask.pocoo.org/), jikji will do re-rendering the template.


## What's good

- **Fast**. Jikji use multiprocessing on generation
- **Expandability**. You can build from micro web to enterprise-class website. 
- **Efficiency**. You can write code fastly with familiar libraries/design pattern.


## Template engine
`Jikji` uses [Jinja2](http://jinja.pocoo.org) template engine which is used in [Flask](http://flask.pocoo.org/) as well.  
You can see Jinja template documentation [here](http://jinja.pocoo.org/docs/dev/templates/).

  
## View-Page Concept

Jikji has a concept `View`, which is similar to `Controller` on common backend frameworks.
One `View` has one 'URL rule', one 'View Function', but multiple 'Pages'.

Usually, the controller has the role of taking the data from the model
with the PARAMETERS in URL and returning the HTML with the View.

In static web, PARAMETERS are provided in advance.
There is many tuple set of parameters in ONE VIEW.

Jikji calls the tuple `Page`


For example, if 'Article View' has url rule `/posts/$1/$2`
the sample PAGEs for 'Article View' would be the following.

```
/posts/dev/best-sublime-text-3-themes-of-2016
/posts/dev/the-best-news-from-angulars-ng-conf
```



