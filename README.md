# Jikji [![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi/jikji) [![Build Status](https://travis-ci.org/Prev/jikji.svg)](https://travis-ci.org/Prev/jikji) 

Python Static website generator for Modern web


## What's different
Common static website generators, like [Jekyll](https://jekyllrb.com/), aim to transform mardowns to HTMLs.

While Jekyll is a blog-friendly generator, Jikji pursues **general purpose** static website generator, allowing a developer to write a code communicating with **DBMS** or **RESTFul API servers**.


## Getting Started

First, install Jikji using pypi.

```bash
$ pip install jikji
```

Then you can use command line interfaces of Jikji.
Try creating a new project.

```bash
$ mkdir myproj
$ cd myproj

$ jikji create .
```

Now you can find several files like below:

```
.
├── settings.py
├── pages.py
├── static
│   ├── images
│   │   ├── ...
│   └── stylesheet.css
├── templates
│   ├── gallery.html
│   └── home.html
└── views
    ├── gallery.py
    └── home.py
```

`settings.py` is the entry point of this project. You can define paths for template, static files, view files, publishers, and init scripts.

`pages.py` is the default init script for sample project. Fixed data list and sample commands are located in this file. You may understand the design patterns of Jikji by reading this file. We give the full file content here:

```python
from jikji import getview, addpage

item_list = [
	{'id': 1, 'image_url': '/images/image1.jpg', 'location': 'Paris, France', 'year': '2018'},
	{'id': 2, 'image_url': '/images/image2.jpg', 'location': 'San Francisco, CA', 'year': '2017'},
	{'id': 3, 'image_url': '/images/image3.jpg', 'location': 'Seattle, WA', 'year': '2018'},
	{'id': 4, 'image_url': '/images/image4.jpg', 'location': 'Seoul, Korea', 'year': '2018'},
	{'id': 5, 'image_url': '/images/image5.jpg', 'location': 'Venice, Italy', 'year': '2017'},
]

getview('home.index').url_rule = '/'
getview('gallery.index').url_rule = '/{id}/'

addpage(view='home.index', params=(item_list,))

for item in item_list:
	addpage(view='gallery.index', params=item)
```

As you can see in the code above, major keywords of Jikji are `view` and `pages`. Simply, `view` is an interface while `page` is an instance of a static web.

In Jikji, `views` works similar with the controller of MVC pattern. Each `view` has one 'URL rule', one 'view function', and multiple `pages`.
For example, `gallery.index` view has the url rule `/{id}/`. And the pages for `gallery.index` view  have actuall URLs like `/1/`, `/2/`, `/3/`, ... Here is the view file for `gallery.index`:

```python
from jikji import render_template, register_view

@register_view
def index(data):
	return render_template('gallery.html',
		image_url=data['image_url'],
		location=data['location'],
		year=data['year'],
	)
```

Note that Jikji uses [Jinja2](http://jinja.pocoo.org) template engine which is used in [Flask](http://flask.pocoo.org/) as well. You can see Jinja template documentation [here](http://jinja.pocoo.org/docs/dev/templates/).


`templates` and `static` directories are similar with Flask or other web frameworks. Then let's talk about the `view`.


## Generate static files

You can generate static files by simply calling command line below:

```bash
$ jikji generate <project_dir>
```

If your project is located in curreny directory, just call:

```bash
$ jikji generate .
```

Our generator uses multiprocess package of python. Thus, note that you have to design your project with side-effect free.



## Open server for testing

On developing step, you don't have to generate all the time after modifying template.
Jikji provides useful feature to develop in realtime.

Run jikji as **listening** mode:

```bash
$ jikji listen <project_dir>
$ jikji listen <project_dir> --port PORT --host HOST
```

Then you can see rendered website in your browser (default: http://localhost:7000). When you reload the website, Jikji will do re-rendering the templates.

Limitations: if you change the init scripts including `settings.py` and `pages.py`, Jikji would not reload the files. In that case, please turn off the server and restart Jikji listening mode.
