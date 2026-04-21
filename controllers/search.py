from extensions import jinja
from services.api_service import get_search_vod_list, get_category_list

async def search_page(request):
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    
    if not keyword:
        categories = await get_category_list()
        return jinja.render('search.html', request, 
                            vod_list=[], 
                            categories=categories,
                            keyword='',
                            total=0,
                            current_page=1,
                            pagecount=1)
    
    data = get_search_vod_list(keyword=keyword, page=page)
    categories = await get_category_list()
    
    vod_list = data.get('list', []) if data else []
    total = data.get('total', 0) if data else 0
    pagecount = data.get('pagecount', 1) if data else 1
    current_page = data.get('page', 1) if data else 1
    
    return jinja.render('search.html', request, 
                        vod_list=vod_list, 
                        categories=categories,
                        keyword=keyword,
                        total=total,
                        current_page=current_page,
                        pagecount=pagecount)