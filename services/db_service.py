import aiomysql
from config import MYSQL_CONFIG

async def get_db_connection():
    return await aiomysql.connect(**MYSQL_CONFIG)

async def sync_categories_from_api(categories):
    conn = None
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cur:
            for cat in categories:
                type_id = cat.get('type_id')
                type_pid = cat.get('type_pid', 0)
                type_name = cat.get('type_name')
                
                if not type_id or not type_name:
                    continue
                
                await cur.execute(
                    "SELECT type_id FROM category WHERE type_id = %s",
                    (type_id,)
                )
                exists = await cur.fetchone()
                
                if exists:
                    await cur.execute(
                        "UPDATE category SET type_pid = %s, type_name = %s WHERE type_id = %s",
                        (type_pid, type_name, type_id)
                    )
                else:
                    await cur.execute(
                        "INSERT INTO category (type_id, type_pid, type_name) VALUES (%s, %s, %s)",
                        (type_id, type_pid, type_name)
                    )
            await conn.commit()
    finally:
        if conn:
            conn.close()

async def get_categories_from_db():
    conn = None
    try:
        conn = await get_db_connection()
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM category ORDER BY type_pid, type_id")
            return await cur.fetchall()
    finally:
        if conn:
            conn.close()

async def get_category_count():
    conn = None
    try:
        conn = await get_db_connection()
        async with conn.cursor() as cur:
            await cur.execute("SELECT COUNT(*) FROM category")
            result = await cur.fetchone()
            return result[0] if result else 0
    finally:
        if conn:
            conn.close()