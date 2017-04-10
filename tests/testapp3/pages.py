from jikji import addpage, addpagegroup
from views.event import EventPageGroup

for i in range(1, 5) :
	addpage(view='people.index', params=(i, ))
	addpage(view='people.comment', params=(i, ))

for i in range(1, 3) :
	addpagegroup(EventPageGroup({'id': i}))
