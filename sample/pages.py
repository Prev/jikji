from jikji import addpage, addpagegroup
from views.event import EventPageGroup

for i in range(1, 5) :
	addpage(view='people.index', params=('group1', 'people%d' % i))
	addpage(view='people.comment', params=('group1', 'people%d' % i))


addpagegroup(EventPageGroup({'id': 3}))
