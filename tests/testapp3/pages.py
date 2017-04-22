from jikji import addpage, addpagegroup
from views.event import EventPageGroup
from views.people import PeoplePageGroup

for i in range(1, 5) :
	addpagegroup(PeoplePageGroup({'id': i}))

for i in range(1, 3) :
	addpagegroup(EventPageGroup({'id': i}))
