# people.py

from jikji import render_template, register_view


@register_view
def index(group_name, people_name) :

	return render_template('people.html',
		group=group_name,
		name=people_name,
		id='%s-%s' % (group_name, people_name)
	)


@register_view
def comment(group_name, people_name) :

	return render_template('people_comment.html',
		id='%s-%s' % (group_name, people_name),
		comments=['Test Comment'],
	)

