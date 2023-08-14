from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def fetch_data(url):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=5)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except asyncio.TimeoutError:
        print(f"Timeout while fetching data from {url}")
    except Exception as e:
        print(f"Error while fetching data from {url}: {e}")
    return []


@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [fetch_data(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    merged_numbers = sorted(list(set([num for sublist in results for num in sublist])))

    return jsonify(numbers=merged_numbers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
