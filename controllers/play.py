from extensions import jinja
from services.api_service import get_play_url, get_category_list

def is_m3u8_url(url):
    if not url:
        return False
    lower_url = url.lower()
    return '.m3u8' in lower_url or 'hls' in lower_url or 'mpegurl' in lower_url

async def play_page(request, vod_id):
    play_index = int(request.args.get('n', 1))
    play_data = get_play_url(vod_id, play_index)
    categories = await get_category_list()
    
    if not play_data:
        return jinja.render('404.html', request)
    
    vod = play_data.get('vod')
    play_url = play_data.get('url', '')
    play_list = play_data.get('list', [])
    sources = play_data.get('sources', [])
    current_source_name = play_data.get('current_source_name', '')
    
    return jinja.render('play.html', request, 
                        vod=vod, 
                        play_url=play_url,
                        play_list=play_list,
                        sources=sources,
                        current_source_name=current_source_name,
                        current_index=play_index,
                        categories=categories,
                        is_m3u8_url=is_m3u8_url)
