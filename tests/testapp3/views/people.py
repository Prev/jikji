from jikji import render_template, register_view
from jikji.view import PageGroup, Page




class PeoplePageGroup(PageGroup) :
	def __init__(self, model) :
		self.model = model
		self.id = model['id']

	def getpages(self) :
		return (
			Page(view=self.index, params=self),
			Page(view='people.comment', params=self),
		)


	@register_view(url_rule='/people/{ id }/')
	def index(self) :
		return render_template('people.html',
			id=self.model['id'],
		)


	@register_view(url_rule='/people/{ model.id }/comment/')
	def comment(self) :
		return render_template('people_comment.html',
			id=self.model['id'],
		)