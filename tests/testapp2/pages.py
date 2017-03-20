from jikji.view import view


view('myview.home').addpage()

view('myview.profile').addpage('Prev', 'https://github.com/Prev')
view('myview.profile').addpage('^_^', 'http://google.com')

view('myview.requirements').addpage()