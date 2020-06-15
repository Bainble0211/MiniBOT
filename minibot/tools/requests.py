import aiohttp

async def reqjson (url : str, header = None) :
   async with aiohttp.ClientSession () as session:
      async with session.get (url, headers=header) as r :
         data = await r.json()
   return data

async def reqtext (url : str, header = None) :
   async with aiohttp.ClientSession () as session:
      async with session.get (url = url, headers=header) as r :
         data = await r.text()
   return data

async def requests (url : str, header = None) :
   async with aiohttp.ClientSession () as session:
      async with session.get (url, headers=header) as r :
         return r
         
