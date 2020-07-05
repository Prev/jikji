from jikji import render_template, register_view

@register_view
def index(item_list):
	return render_template('home.html', item_list=item_list)
