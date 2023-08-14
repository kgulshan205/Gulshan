from flask import Flask, request, jsonify
import aiohttp
import asyncio

app = Flask(__name__)

async def fetch_data(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("numbers", [])
    except asyncio.TimeoutError:
        print(f"Timeout while fetching data from {url}")
    except Exception as e:
        print(f"Error while fetching data from {url}: {e}")
    return []

async def fetch_all_data(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    results = loop.run_until_complete(fetch_all_data(urls))
    loop.close()

    merged_numbers = sorted(list(set([num for sublist in results for num in sublist])))

    return jsonify(numbers=merged_numbers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
