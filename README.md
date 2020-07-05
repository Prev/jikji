# Jikji [![Pypi](https://img.shields.io/pypi/v/jikji.svg)](https://pypi.python.org/pypi/jikji) [![Build Status](https://travis-ci.org/Prev/jikji.svg)](https://travis-ci.org/Prev/jikji) 

Python Static website generator for Modern web


## What's different
Common static website generators, like [Jekyll](https://jekyllrb.com/), usually aim to transform markdowns to HTMLs. On the other hand, Jikji gets `code` for generating HTMLs instead of static markdowns.

Furthermore, common static website generators are blog-friendly, but Jikji pursues **general purpose** static website generator, by allowing developers to write the code communicating with **DBMS** or **RESTFul API servers**.

Are you interested in code-based static web site generator, follow the "Getting Started" section. You may like it.


## Getting Started

First, install Jikji using pypi.

```bash
$ pip install jikji
```

Then you can use command line interfaces of Jikji.
Try creating a new project.

```bash
$ jikji create myproj
$ cd myproj
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

`settings.py` is the entry point of this project. You can define paths for template, static files, view files, and init scripts.

`pages.py` is the default init script for sample project. Fixed sample data and configuration for the website are located in this file. You may understand the design patterns of Jikji by reading this file. We give the full file content here:

```python
# pages.py
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
For example, `gallery.index` view has the url rule `/{id}/`, and five pages that have actuall URLs like `/1/`, `/2/`, `/3/`, ...
And the view functions are defined in `/views`. Here is the view file for `gallery.index`:

```python
# views/gallery.py
from jikji import render_template, register_view

@register_view
def index(data):
	return render_template('gallery.html',
		image_url=data['image_url'],
		location=data['location'],
		year=data['year'],
	)
```

Note that Jikji uses [Jinja2](http://jinja.pocoo.org) template engine, which is used in [Flask](http://flask.pocoo.org/) as well. You can see Jinja template documentation in [here](http://jinja.pocoo.org/docs/dev/templates/).


`templates` and `static` directories are similar with Flask or other web frameworks.
You can change the name of these directories in `settings.py`.


## Generate static files

You can generate static files by simply calling command line below:

```bash
$ jikji generate <project_dir>
```

If your project is located in curreny directory, just call:

```bash
$ jikji generate .
```

Then you can see the result in `output` directory. If you want to change it, open `settings.py`.

Note that our generator uses multiprocessing package of Python. Thus, you have to design your project with **side-effect free**.



## Open server for testing

On developing stage, you don't have to generate all the time after modifying templates.
Jikji provides a useful feature for developing in realtime.

Run jikji as **listening** mode:

```bash
$ jikji listen <project_dir>
$ jikji listen <project_dir> --port PORT --host HOST
```

You can see the rendered website in your browser (default: http://localhost:7000) after running the listening mode. When you reload the website, Jikji will do re-rendering the templates.

Limitations: if you change the init scripts including `settings.py` and `pages.py`, Jikji would not reload the files. In that case, please turn off the server and restart Jikji listening mode.


## Contributions

Any contributions are welcome. Or, if you have any question while using Jikji, feel free to ask a question.


