from jikji import getview, addpage


getview('myview.myview').url_rule = '/$1.html'

for i in range(1, 5) :
	addpage(view='myview.myview', params=(i,))