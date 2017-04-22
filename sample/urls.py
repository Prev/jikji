from jikji import getview

getview('people.index').url_rule = '/$1/$2/'
getview('people.comment').url_rule = '/$1/$2/comment/'