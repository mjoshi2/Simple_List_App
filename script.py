import requests
#import urllib2
from bs4 import BeautifulSoup

r = requests.get('http://192.168.114.135:5000')
resp = BeautifulSoup(r.text)
print resp.get_text()


r_show = requests.get('http://192.168.114.135:5000/show')
resp_show = BeautifulSoup(r_show.text)
print resp_show.get_text()

item = {'description':'Send grandma a birthday card','to_be_done_by':' tomorrow'}
r_add = requests.post('http://192.168.114.135:5000/add', data=item)
#resp_show = BeautifulSoup(r_show.text)
#print resp_show.get_text()

r_show = requests.get('http://192.168.114.135:5000/show')
resp_show = BeautifulSoup(r_show.text)
print resp_show.get_text()

r_del = requests.get('http://192.168.114.135:5000/delete/1')
resp_del = BeautifulSoup(r_del.text)
print resp_del.get_text()

r_clear = requests.get('http://192.168.114.135:5000/clear')
resp_clear = BeautifulSoup(r_clear.text)
print resp_clear.get_text()
