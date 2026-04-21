from extensions import jinja
from services.api_service import get_category_vod_list, get_category_list

async def category_list(request, type_id):
    page = int(request.args.get('page', 1))
    
    data = get_category_vod_list(type_id=type_id, page=page)
    categories = await get_category_list()
    
    vod_list = data.get('list', []) if data else []
    total = data.get('total', 0) if data else 0
    pagecount = data.get('pagecount', 1) if data else 1
    current_page = int(data.get('page', 1)) if data else 1
    
    current_category = next((cat for cat in categories if cat.get('type_id') == int(type_id)), None)
    category_name = current_category.get('type_name') if current_category else '未知分类'
    
    return jinja.render('category.html', request, 
                        vod_list=vod_list, 
                        categories=categories,
                        category_name=category_name,
                        type_id=type_id,
                        total=total,
                        pagecount=pagecount,
                        current_page=current_page)