from jikji.view import render_template, view

@view(url_rule='/$1.html')
def myview(num) :
	return render_template('template1.html', n=num)