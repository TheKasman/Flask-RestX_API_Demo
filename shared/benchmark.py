import asyncio
import httpx
import time
import sys

CONCURRENT_REQUESTS = 5
ITEM_ID = 32 #Using a known weapon id with dice

# This is just the message being fired
async def fire_request(client, url):
    start = time.time()
    response = await client.get(url)
    elapsed = time.time() - start
    print(f" -> {response.status_code} in {elapsed:.2f}s")
    return elapsed

#now for the good stuff, FIRE ALL BLASTERS
async def run_benchmark(base_url, label):
    url = f"{base_url}/items/{ITEM_ID}/roll"
    print(f"\n--- {label} ({CONCURRENT_REQUESTS} concurrent requests) ---")

    async with httpx.AsyncClient(timeout=60.0) as client:
        start = time.time()
        tasks = [fire_request(client, url) for _ in range(CONCURRENT_REQUESTS)]
        await asyncio.gather(*tasks)
        total = time.time() - start

    print(f"TOTAL wall-clock time: {total:.2f}s")
    return total

# we get to choose whether or not we use flask or fastapi when we run the benchmark
async def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "flask"

    if target == "flask":
        await run_benchmark("http://localhost:8000", "Flask (sync)")
    elif target == "fastapi":
        await run_benchmark("http://localhost:8001", "FastAPI (async)")
    else:
        print("Usage: python -m shared.benchmark [flask|fastapi]")

if __name__ == "__main__":
    asyncio.run(main())
