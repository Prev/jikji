# people.py

from jikji import render_template, register_view


@register_view(url_rule='/people/$1/')
def index(id) :
	return render_template('people.html',
		id=id,
	)


@register_view(url_rule='/people/$1/comment/')
def comment(id) :
	return render_template('people_comment.html',
		id=id
	)

