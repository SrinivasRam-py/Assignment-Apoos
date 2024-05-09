# Question 1: Asynchronous I/O with Memory Optimization (15 minutes)
 
# Task: Develop a Python script that efficiently downloads a list of URLs concurrently while minimizing memory usage. The script should:
 
# Accept a list of URLs as input.
# Use asynchronous I/O techniques (e.g., asyncio, aiohttp) to download the content of each URL concurrently.
# Employ techniques to limit the number of concurrent downloads to prevent overwhelming system resources. Consider using a semaphore or similar mechanism.
# Print the downloaded content for each URL or an error message if the download fails.
 
# Question 2: Advanced Decorator Design with Caching and Metaprogramming (15 minutes)
 
# Task: Create a decorator in Python that:
 
# Caches the results of a function based on its arguments.
# Leverages metaprogramming techniques (e.g., inspect module) to automatically determine the function's signature (argument names) for cache key generation.
# Provides a configuration option to specify the maximum cache size or a time-based expiration for cached values.
# Optionally integrates with a persistent cache storage mechanism (e.g., Redis, in-memory database) for scalability.


# task1
import aiohttp
import asyncio

async def fetch_content(session,url,semaphore):
    async with semaphore:
        try:
            async with session.get(url) as response:
                content = await response.text()
                print("downloaded content from {url}:{content[:50]}")
        except aiohttp.ClientError as e:
            print("error downloading content from {url}:{e}")
            
async def download_urls(urls):
    semaphore = asyncio.Semaphore(10)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_content(session,url,semaphore) for url in urls]
        await asyncio.gather(*tasks)
        
if __name__ == "__main__":
    urls = [
        "https://example.com"
    ]
    
asyncio.run(download_urls(urls))



#task 2 

import functools
import pickle

def memoize(max_size,persistent_cache):
    def decorator(func):
        cache = {}
        if persistent_cache:
            try:
                with open(persistent_cache,'rb')as file:
                    cache = pickle.load(file)
            except FileNotFoundError:
                pass
            
            
        def wrapper(*args,**kwargs):
            key = args+tuple(sorted(kwargs.item()))
            if key not in cache:
                result = func(*args,**kwargs)
                cache[key] = result
            if persistent_cache:
                with open(persistent_cache,'wb')as file:
                    pickle.dump(cache,file)
                    
            return cache[key]
        
        return wrapper
    return decorator

@memoize(max_size=100,persistent_cache="cache.pk1")
def expensive_function(x,y):
    print("....")
    return x+y

print(expensive_function(1,2))
