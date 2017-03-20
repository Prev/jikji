from jikji.view import view

view('myview.myview').url_rule = '/$1.html'

for i in range(1, 5) :
	view('myview.myview').addpage(i)