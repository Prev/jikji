from jikji import render_template, register_view
from jikji.view import PageGroup, Page


@register_view(url_rule='/event/$1')
def index(event_id) :
	return '<div>Event: %s</div>' % event_id



@register_view(url_rule='/event/comment/$1')
def comment(event_id) :
	return '<div>Event Comment: %s</div>' % event_id



class EventPageGroup(PageGroup) :
	def __init__(self, model) :
		self.model = model
		self.id = model['id']


	# @group_view()
	# def comment(event_id) :
	# 	return '<div>Event Comment: %s</div>' % event_id


	def getpages(self) :
		return (
			Page(view='event.index', params=(self.id, )),
			Page(view='event.comment', params=(self.id, )),
		)


	def before_rendered(self) :
		pass

	def after_rendered(self) :
		pass