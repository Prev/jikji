# people.py

from jikji.view import render_template, view, meta


@view
def index(group_name, people_name) :
	context = {
		'group': group_name,
		'name': people_name,
		'id': '%s-%s' % (group_name, people_name)
	}

	return render_template('people.html', context)


@view
def comment(group_name, people_name) :
	context = {
		'id': '%s-%s' % (group_name, people_name),
		'comments': ['Test Comment']
	}

	return render_template('people_comment.html', context)

