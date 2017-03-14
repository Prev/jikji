from jikji.view import view

# url_rules = {}

# url_rules['people.index'] = '/$1/$2'
# url_rules['people.comment'] = '/$1/$2/comment'


view('people.index').url_rule = '/$1/$2/'
view('people.comment').url_rule = '/$1/$2/comment/'