from jikji.view import view


for i in range(1, 5) :
	#view('people.index').addpage('group1', 'people%d' % i)
	#view('people.comment').addpage('group1', 'people%d' % i)
	view('people.people').adddata({'i': i})
