from jikji import render_template, register_view

# FYI, `register_view` decorator accepts `url_rule`.
# Instead of defining url rules on `pages.py`, you can define each view files.
# It just depends on your preference, but make sure not to define redundantly.
#
# @register_view(url_rule='/{id}/')
@register_view
def index(data):
	return render_template('gallery.html',
		image_url=data['image_url'],
		location=data['location'],
		year=data['year'],
	)

