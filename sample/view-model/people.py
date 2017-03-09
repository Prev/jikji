# people.py

def index(group_name, people_name) :
	#url = 'http://api.memento.live/people/%s/%s' % (group_name, people_name)
	#context = requests.get(url)

	context = {
		'group': group_name,
		'name': people_name,
		'id': '%s-%s' % (group_name, people_name)
	}

	return context

def comment(group_name, people_name) :
	return {
		'id': '%s-%s' % (group_name, people_name),
		'comments': ['Test Comment']
	}

