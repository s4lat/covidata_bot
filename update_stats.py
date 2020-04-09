# -*- coding: utf-8 -*-
import requests as req
import json, imgkit, os, logging

logging.basicConfig(filename='log.log',level=logging.INFO)

with open('page.html') as f:
		template = f.read()

template = template.replace("#RESETCSS", os.path.abspath('./static/reset.css'))
template = template.replace("#BOOTSTRAP", os.path.abspath('./static/bootstrap_4.0.0/css/bootstrap.min.css'))

imgkit_options = {
    	'quiet': '',
    	'width': '768',
    	"xvfb": ""
    	}

with open('secret.token') as f:
		TOKEN = f.read().split()[0]

stats_url = "https://covid-193.p.rapidapi.com/statistics"
countries_urls = "https://covid-193.p.rapidapi.com/countries"

headers = {
		'x-rapidapi-host': "covid-193.p.rapidapi.com",
		'x-rapidapi-key': TOKEN
		}

def get_data():
	resp = req.request("GET", stats_url, headers=headers)
	data = json.loads(resp.text)

	while data['errors']:
		resp = req.request("GET", stats_url, headers=headers)
		data = json.loads(resp.text)

	data['response'] = [d for d in data['response'] if d['country'] != 'All']

	return data['response']

def update_pages(*args):
	data = get_data()

	data = sorted(data, key=lambda k: k['cases']['active'], reverse=True)
	
	pages = []
	c = 1
	html = template
	for i, d in enumerate(data):
		html = html.replace('#IND', str(i), 1)
		html = html.replace('#Country', str(d['country']), 1)
		html = html.replace('#Active', str(d['cases']['active']), 1)

		if d['cases']['new']:
			if int(d['cases']['new']) <= 0:
				html = html.replace('#NACOLOR', 'rgb(25, 200, 0)', 1)
				html = html.replace('#NA', d['cases']['new'], 1)
			else:
				html = html.replace('#NACOLOR', 'rgb(255, 25, 0)', 1)
				html = html.replace('#NA', d['cases']['new'], 1)
		else:
			html = html.replace('#NACOLOR', '', 1)
			html = html.replace('[#NA]', '', 1)


		html = html.replace('#Recovered', str(d['cases']['recovered']), 1)
		html = html.replace('#Deaths', str(d['deaths']['total']), 1)

		if  d['deaths']['new']:
			if int(d['deaths']['new']) <= 0:
				html = html.replace('#NDCOLOR', 'rgb(25, 200, 0)', 1)
				html = html.replace('#ND', d['deaths']['new'], 1)
			else:
				html = html.replace('#NDCOLOR', 'rgb(255, 25, 0)', 1)
				html = html.replace('#ND', d['deaths']['new'], 1)
		else:
			html = html.replace('#NDCOLOR', '', 1)
			html = html.replace('[#ND]', '', 1)


		html = html.replace('#Total', str(d['cases']['total']), 1)
		if (i+1) % 10 == 0:
			imgkit.from_string(html, 'pages/out%s.jpg' % c, options=imgkit_options)
			html = template
			c += 1

	if html != template:
		html = html.replace('#Country', '')
		html = html.replace('#Active', '')
		html = html.replace('#Recovered', '')
		html = html.replace('#Deaths', '')
		html = html.replace('#Total', '')
		html = html.replace('#IND', '')
		html = html.replace('[#ND]', '')
		html = html.replace('[#NA]', '')

		imgkit.from_string(html, 'pages/out%s.jpg' % c, options=imgkit_options)

	logging.info("[INFO] Successfully updated all pages")


