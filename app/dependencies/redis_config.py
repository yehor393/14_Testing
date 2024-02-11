# import aioredis

# REDIS_URL = "redis://localhost:6379"

# async def create_redis_pool():
#     # Створення Redis пулу
#     pool = await aioredis.create_redis_pool(REDIS_URL)
#     return pool

# async def get_redis(pool):
#     # Отримання Redis з пулу
#     async with pool.get() as conn:
#         return conn
