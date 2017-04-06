from jikji import addpage

for i in range(1, 5) :
	addpage(view='people.index', params=('group1', 'people%d' % i))
	addpage(view='people.comment', params=('group1', 'people%d' % i))


