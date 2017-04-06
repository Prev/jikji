from jikji import getview


getview('myview.home').url_rule = '/'
getview('myview.profile').url_rule = '/$1/'
getview('myview.requirements').url_rule = '/requirements.txt'