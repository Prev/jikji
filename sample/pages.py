from jikji.view import makeviews, view

makeviews((
	('people.index', '/$1/$2/', 'people.html'),
	('people.comment', '/$1/$2/comment/', 'people_comment.html')
))


for i in range(1, 5) :
	view('people.index').addpage('group1', 'people%d' % i)
	view('people.comment').addpage('group1', 'people%d' % i)
