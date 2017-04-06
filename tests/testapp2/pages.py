from jikji import addpage


addpage(view='myview.home')

addpage(view='myview.profile', params=('Prev', 'https://github.com/Prev'))
addpage(view='myview.profile', params=('^_^', 'http://google.com'))

addpage(view='myview.requirements', params=())