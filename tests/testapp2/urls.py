from jikji.view import view


view('myview.home').url_rule = '/'
view('myview.profile').url_rule = '/$1/'
view('myview.requirements').url_rule = '/requirements.txt'