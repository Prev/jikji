# Jikji
[![Build Status](https://travis-ci.org/Prev/jikji.svg?branch=master)](https://travis-ci.org/Prev/jikji)  


Code-less static web generator based on RESTFul API Server

First, web site needs `view` template file like **html**.
Then, it needs `model` that will be injected to template's **context**. In `jikji`, we use `model` as remote RESTFul API Server like [cloudant](https://cloudant.com/).

**Code** for getting data from `model` and generate `template` file is **NOT** needed (Simply, `Controller` code is NOT needed).


## Usage
```bash
$ pip install jikji
$ python3 -m jikji sample_site
```

or

```python
from jikji import Jikji
jikji = Jikji('sample_site')
jikji.generate()
```

  
## config.json
Configure directory structure of site, and rest api server's information.

#### example
```json
{
	"rest_server": {
		"type": "cloudant",
		"base_url": "https://rexpress.cloudant.com/",
		"headers": {
			"Authorization": "Basic aGVsbG93b3JsZDpoZWxsb3dvcmxkMTIz="
		}
	},
	"path": {
		"template": "templates",
		"output": "generated",
		"assets": [
			"assets"
		]
	},
	"pages_xml": "pages.xml"
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

You can use `model` variable in pages.xml, which you can connect to `rest-server` db.
After getting data in rest-server, you can make `page tag` with this data.

  

#### example

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<site>
	{% set all_docs = model.get('/test/_all_docs') %}
	<page>
		<url>/</url>
		<context>{{ all_docs }}</context>
		<template>home.html</template>
	</page>
	{% for row in all_docs['rows'] %}
	<page>
		<url>/doc/{{ row['id'] }}/</url>
		<context>{{ model.get('/test/' + row['id']) }}</context>
		<template>document.html</template>
	</page>
	{% endfor %}
</site>
```

After template is rendered by jinja, `jikji` read rendered file and generate static web site. Template files used in static page are also rendered with `jinja`.  
Data written on `context` tag will be injected in process of rendering.


