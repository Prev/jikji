# Jikji
[![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi)
[![Build Status](https://travis-ci.org/Prev/jikji.svg?branch=master)](https://travis-ci.org/Prev/jikji)  

Static website generator based on RESTFul Server

  

## What's different
In common static website generator like [Jekyll](https://jekyllrb.com/),   it transform **plain text** like mardown to html.

  

But `jikji` generate pages based on **JSON** data returned in RESTFul Server.

You can use "Rest-base Cloud Database" like [IBM Cloudant](https://cloudant.com/) as RESTFul Server, 
so you don't need to code RESTFul server yourself.


We call the JSON data that gotten from RESTFul Server `model`.  
After getting `model`, you can access it in template like `{{ article_content }}`.


**Code** for getting data from `model` and generate `template` is **NOT** needed.  
You just write some configs and templates of website, then `jikji` will create static website greatly.


## Install
```bash
$ pip install jikji
```


## Usage
```bash
$ jikji <my_site> generate
```
or
```python
from jikji import Jikji
jikji = Jikji('my_site')
jikji.generate()
```


## template engine
`jikji` use [Jinja2](http://jinja.pocoo.org) template engine which is used in [Flask](http://flask.pocoo.org/).  
You can see jinja template documentation on [here](http://jinja.pocoo.org/docs/dev/templates/).

  
## config.json
Configure directory structure of site, and rest api server's information.

```json
{
	"server_info": {
		"type": "cloudant",
		"baseurl": "https://rexpress.cloudant.com/",
		"headers": {
			"Authorization": "Basic aGVsbG93b3JsZDpoZWxsb3dvcmxkMTIz="
		}
	},
	"path": {
		"template": "templates",
		"output": "generated",
		"assets": [
			"assets"
		],
		"pages_xml": "pages.xml"
	}
}
```

  

## pages.xml
Config pages of static website.
Each `page tag` generates one static website, and it has 3 properties.


- `url` is URL of each output static page.
	- If url is ends with '/', $path/index.html will be generated
- `context` is data object used in template, getting from cloudant.
- `template` is path of html template file.


Specially, `pages.xml` is also parsed like template. So, in `pages.xml`, you can use `for`, `foreach`, `if`, and other grammars.

You can use `model` variable in pages.xml, which you can connect to **RESTFul Server**.
After getting data in RESTFul Server, you can make **page tag** with model data like below.


```xml
<?xml version="1.0" encoding="UTF-8" ?>
<site>
	{% set all_docs = model.get('/_all_docs') %}
	<page>
		<url>/</url>
		<context>{{ all_docs }}</context>
		<template>home.html</template>
	</page>
	{% for id in all_docs.rows %}
	<page>
		<url>/doc/{{ id }}/</url>
		<context>{{ model.get('/doc/' + id) }}</context>
		<template>document.html</template>
	</page>
	{% endfor %}
</site>
```

After template is rendered, `jikji` generate pages by this information.

First, generator get template file declared in `template` tag.  
And then, inject `context` data to template and render it.  
Finally, create static page file with name declared in `url` tag.

You can look sample 


#### sample response of /_all_docs
```json
{
	"site": "Sample site",
	"rows": [
		"a69425f9d9dc1b",
		"ca3dfe24aaeca0"
	]
}
```
#### rendered pages of sample
- /index.html
- /doc/a69425f9d9dc1b/index.html
- /doc/ca3dfe24aaeca0/index.html

  


# Realtime develop
You don't have to generate all the time after modify template.  
`Jikji` has useful function to develop in realtime


run jikji as __listening__ mode

```bash
$ jikji <my_site> listen
$ jikji <my_site> listen --port PORT --host HOST
```

Then you can see rendered website in your browser (default: http://localhost:7000)

Web server opened with [Flask](http://flask.pocoo.org/), and when you reload the website, jikji will re-rendering template


But one server is opened, jikji **DO NOT** reload **MODEL** from rest server.  
Please close flask server if you need to reload model data.


