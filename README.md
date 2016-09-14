# Jikji
Code-less static web generator based on RESTful API Server


## concept
- Model : RESTFul API Server (You can `cloudant`)
- Controller: None
- View: template html


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
		"output": "generated"
	},
	"pages_xml": "pages.xml"
}
```


## pages.xml
This is file to config generating static website.
Each `page tag` generate one static website, and it has 3 properties.


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

After template is render by jinja, `jikji` read rendered file and generate static web site. Template files used in static page are also rendered with `jinja`.  
Data written in `context` tag will be injected in process of rendering.


