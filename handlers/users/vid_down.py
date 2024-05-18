import logging
import time
import re
import json
from aiohttp import ClientSession
import aiohttp
from bs4 import BeautifulSoup
import random
import asyncio
import json,requests

def random_ip():
    ips = ['46.227.123.', '37.110.212.', '46.255.69.', '62.209.128.', '37.110.214.', '31.135.209.', '37.110.213.']
    prefix = random.choice(ips)
    return prefix + str(random.randint(1, 255))

class Downloads:
    @staticmethod
    async def instagram(url):
        result = []
        RES = {}
        data = {'q': url, 'vt': 'home'}
        headers = {
            'origin': 'https://snapinsta.io',
            'referer': 'https://snapinsta.io/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'X-Forwarded-For': random_ip(),
            'X-Client-IP': random_ip(),
            'X-Real-IP': random_ip(),
            'X-Forwarded-Host': 'snapinsta.io'
        }
        base_url = 'https://snapinsta.io/api/ajaxSearch'
        async with aiohttp.ClientSession() as session:
            async with session.post(base_url, data=data, headers=headers) as response:
                jsonn = await response.json()
                if jsonn['status'] == 'ok':
                    if 'data' in jsonn:
                        data = jsonn['data']
                        soup = BeautifulSoup(data, 'html.parser')
                        for i in soup.find_all('div', class_='download-items__btn'):
                            url = i.find('a')['href']
                            result.append({'url': url})
                        RES = {'status': True, 'result': result}
                else:
                    RES = {'status': False, 'result': 'Error'}
                return RES

    @staticmethod
    async def tiktok(url):
        result = []
        data = {'q': url, 'vt': 'home'}
        RES = {}
        headers = {
            'origin': 'https://snaptik.net',
            'referer': 'https://snaptik.net/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'X-Forwarded-For': random_ip(),
            'X-Client-IP': random_ip(),
            'X-Real-IP': random_ip(),
            'X-Forwarded-Host': 'snaptik.net'
        }
        base_url = f'https://snaptik.net/api/AjaxSearch'
        async with aiohttp.ClientSession() as session:
            async with session.post(base_url, data=data, headers=headers) as response:
                jsonn = await response.json()
                if jsonn['status'] == 'ok':
                    if 'data' in jsonn:
                        data = jsonn['data']
                        soup = BeautifulSoup(data, 'html.parser')
                        for i in soup.find_all('div', class_='dl-action'):
                            url = i.find('a')['href']
                            result.append({'url': url})
                        RES = {'status': True, 'result': result}
                else:
                    RES = {'status': False, 'result': 'Error'}
                return RES
    @staticmethod
    async def snapchat(url):
        static_url = "https://download-snapchat-video-spotlight-online.p.rapidapi.com/download"

        querystring = {"url":url}

        headers = {
            "X-RapidAPI-Key": "1652fa5538msh75884d19fe15282p12b470jsn8487ebe74caa",
            "X-RapidAPI-Host": "download-snapchat-video-spotlight-online.p.rapidapi.com"
        }

        try:
            response = requests.get(static_url, headers=headers, params=querystring)
            if response.status_code == 200:
                data = response.json()
                return {'status': True, 'result': data}
            else:
                return {'status': False, 'result': 'Error'}
        except Exception as e:
            return {'status': False, 'result': f'Error: {str(e)}'}