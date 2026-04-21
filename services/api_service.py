import requests
import json
import redis
from config import API_URL, REDIS_CONFIG, CACHE_EXPIRE
from services.db_service import get_categories_from_db, sync_categories_from_api, get_category_count

redis_client = redis.Redis(**REDIS_CONFIG)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36'}

def fetch_api_data(params=None):
    url = API_URL
    if params:
        url += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    cache_key = f"api:{url}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    try:
        response = requests.get(url,headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        redis_client.setex(cache_key, CACHE_EXPIRE, json.dumps(data))
        return data
    except Exception as e:
        print(f"API request failed: {e}")
        return None

def get_homepage_data():
    data = fetch_api_data()
    if data and data.get('code') == 1:
        return data
    return None

async def get_category_list():
    count = await get_category_count()
    if count > 0:
        return await get_categories_from_db()
    
    data = fetch_api_data()
    if data and data.get('code') == 1:
        categories = data.get('class', [])
        if categories:
            await sync_categories_from_api(categories)
        return categories
    return []

def get_homepage_vod_list(page=1):
    params = {'pg': page,'ac':'detail'}
    data = fetch_api_data(params)
    if data and data.get('code') == 1:
        return data
    return None

def get_category_vod_list(type_id, page=1):
    params = {'pg': page, 't': type_id,'ac':'detail'}
    data = fetch_api_data(params)
    if data and data.get('code') == 1:
        return data
    return None

def get_search_vod_list(keyword, page=1):
    params = {'page': page, 'wd': keyword,'ac':'detail'}
    data = fetch_api_data(params)
    if data and data.get('code') == 1:
        return data
    return None

def get_vod_detail(vod_id):
    params = {'ac': 'detail', 'ids': vod_id}
    data = fetch_api_data(params)
    if data and data.get('code') == 1:
        return data.get('list', [])[0] if data.get('list') else None
    return None

def parse_play_urls(vod_detail):
    play_url = vod_detail.get('vod_play_url', '')
    play_from = vod_detail.get('vod_play_from', '')
    
    play_sources = play_from.split('$$$')
    play_url_parts = play_url.split('$$$')
    
    sources = []
    for i, source_name in enumerate(play_sources):
        if i < len(play_url_parts):
            episodes = []
            url_list = play_url_parts[i].split('#')
            for item in url_list:
                if '$' in item:
                    parts = item.split('$', 1)
                    if len(parts) == 2:
                        episodes.append({
                            'name': parts[0].strip(),
                            'url': parts[1].strip(),
                            'n': len(episodes) + 1
                        })
            sources.append({
                'name': source_name,
                'episodes': episodes
            })
    
    return sources

def get_play_url(vod_id, play_index=1):
    vod_detail = get_vod_detail(vod_id)
    if not vod_detail:
        return None
    
    sources = parse_play_urls(vod_detail)
    
    if sources:
        preferred_source = None
        for source in sources:
            if 'm3u8' in source['name'].lower():
                preferred_source = source
                break
        
        if not preferred_source:
            preferred_source = sources[0]
        
        if preferred_source['episodes'] and play_index <= len(preferred_source['episodes']):
            play_url = preferred_source['episodes'][play_index-1]['url']
            return {
                'url': play_url,
                'list': preferred_source['episodes'],
                'sources': sources,
                'vod': vod_detail,
                'current_source_name': preferred_source['name']
            }
    
    return None
