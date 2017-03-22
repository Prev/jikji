from jikji.view import render_template, view
from models import mymodel

@view
def home() :
	return render_template('home.html')


@view
def profile(name, siteurl) :
	return render_template('profile.html', {
		'name': name,
		'siteurl': siteurl,
		'model': mymodel,
	})


@view
def requirements() :
	return 'jikji>=2.0\nrequests>=2.11'