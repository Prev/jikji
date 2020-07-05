from jikji import getview, addpage

# It is a sample data for this project.
# You can call API using http, or fetching data from RDBMS instead of fixed data.
item_list = [
	{'id': 1, 'image_url': '/images/image1.jpg', 'location': 'Paris, France', 'year': '2018'},
	{'id': 2, 'image_url': '/images/image2.jpg', 'location': 'San Francisco, CA', 'year': '2017'},
	{'id': 3, 'image_url': '/images/image3.jpg', 'location': 'Seattle, WA', 'year': '2018'},
	{'id': 4, 'image_url': '/images/image4.jpg', 'location': 'Seoul, Korea', 'year': '2018'},
	{'id': 5, 'image_url': '/images/image5.jpg', 'location': 'Venice, Italy', 'year': '2017'},
]

# In Jikji, `view` works similar with controller of MVC pattern.
# Defining URL rule of the views can be done like below.
getview('home.index').url_rule = '/'

# If you pass a single dict object to the params, you can use property on the url rule.
getview('gallery.index').url_rule = '/{id}/'

# If you pass list object to the params, you can use '${number}' operator on the url rule.
# For example, you may call the function `addpage` with params `[article_id, user_id, article_data]`,
# then you can define url rule like below:
# getview('article.index').url_rule = '/articles/$1/$2/'


# Now you have to call `addpage` for the views.
# Jikji will automatically generate the pages by calling view functions with given params.
for item in item_list:
	addpage(view='gallery.index', params=item)

# Note that if you want to pass a **single list-type param**, embrace it with a tuple or a list.
# Otherwise, jikji will try to decompose the list to multiple params, e.g.,
# params=['a', 'b', 'c'] => index('a', 'b', 'c'), while you may want
# params=(['a', 'b', 'c'],) => index(['a', 'b', 'c']).
addpage(view='home.index', params=(item_list,))
