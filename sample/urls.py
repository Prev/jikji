from jikji import getview

# url_rules = {}

# url_rules['people.index'] = '/$1/$2'
# url_rules['people.comment'] = '/$1/$2/comment'


getview('people.index').url_rule = '/$1/$2/'
getview('people.comment').url_rule = '/$1/$2/comment/'