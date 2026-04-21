from extensions import jinja
from services.api_service import get_homepage_vod_list, get_category_list

async def homepage(request):
    page = int(request.args.get('page', 1))
    data = get_homepage_vod_list(page=page)
    categories = await get_category_list()
    
    vod_list = data.get('list', []) if data else []
    total = data.get('total', 0) if data else 0
    pagecount = data.get('pagecount', 1) if data else 1
    current_page = int(data.get('page', 1)) if data else 1
    
    return jinja.render('index.html', request, 
                        vod_list=vod_list, 
                        categories=categories, 
                        total=total,
                        pagecount=pagecount,
                        current_page=current_page)