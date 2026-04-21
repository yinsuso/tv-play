from sanic import Sanic
from extensions import jinja
from controllers.home import homepage
from controllers.category import category_list
from controllers.play import play_page
from controllers.search import search_page

app = Sanic("MovieSite")

jinja.init_app(app)

app.static('/static', './static')

app.add_route(homepage, '/', name='home')
app.add_route(category_list, '/category/<type_id>', name='category')
app.add_route(play_page, '/play/<vod_id>', name='play')
app.add_route(search_page, '/search', name='search')

@app.exception(404)
async def not_found(request, exception):
    return jinja.render('404.html', request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30001, debug=True)
