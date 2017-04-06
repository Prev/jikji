from jikji import render_template, register_view

@register_view(url_rule='/$1.html')
def myview(num) :
	return render_template('template1.html', n=num)