# people.py

from jikji.view import render_template, view, virtualview


@view
def index(group_name, people_name) :
	return render_template('people.html',
		group=group_name,
		name=people_name,
		id='%s-%s' % (group_name, people_name),
	)


@view
def comment(group_name, people_name) :
	return render_template('people_comment.html',
		id='%s-%s' % (group_name, people_name),
		comments=['Test Comment'],
	)



@virtualview
def people(data) :
	return (
		('people.index',	'group1', 'people%d' % data['i']),
		('people.comment',	'group1', 'people%d' % data['i']),
	)