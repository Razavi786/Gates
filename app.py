from flask import Flask,request
from shopify import shopify
from stripeAuth import stripeAuth
import httpx
import asyncio
import time

app = Flask("Gates APIS")

@app.route("/api/shopify")
async def auto_shopify():
	site = request.args.get("site")
	card = request.args.get("cc")
	if not site or not card:
		return {
			"error":"Please Provide The Parameters Correctly",
			"example":"/api/shopify?site=https://www.donata.co&cc=4242424242424242|02|28|000"
			}
	client = httpx.AsyncClient(timeout=30)
	try:
		t = time.perf_counter()
		response,price = await shopify(site,card,client)
		return {
			"card":card,
			"response":response,
			"price":price,
			"taken":f"{(time.perf_counter()-t):.2f}",
			"developer":"@ItzMeSahid"
			}
	except Exception as e:
		return {
			"error":str(e)
			}
	finally:
		await client.aclose()

@app.route("/api/stripe")
async def stripe_auth():
	card = request.args.get("cc")
	if not card:
		return {
			"error":"Please Provide The Parameters Correctly",
			"example":"/api/stripe?cc=4242424242424242|02|28|000"
			}
	client = httpx.AsyncClient(timeout=30)
	try:
		t = time.perf_counter()
		response = await stripeAuth(card,client)
		return {
			"card":card,
			"response":response,
			"taken":f"{(time.perf_counter()-t):.2f}",
			"developer":"@ItzMeSahid"
			}
	except Exception as e:
		return {
			"error":str(e)
			}
	finally:
		await client.aclose()

asyncio.run(app.run(host="0.0.0.0",port=10000))
