from jikji import render_template, register_view
from models import mymodel

@register_view
def home() :
	return render_template('home')


@register_view
def profile(name, siteurl) :
	return render_template('profile.html',
		data={
			'name': name,
			'siteurl': siteurl,
		},
		model=mymodel,
	)


@register_view
def requirements() :
	return 'jikji>=2.0\nrequests>=2.11'