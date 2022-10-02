#install requred modules
!pip install ultimate-sitemap-parser

import threading, os
from usp.tree import sitemap_tree_for_homepage

os.mkdir('urls')
bad_domains = []

def parse_sitemap(domain):
  domain = domain.strip()
  url = f'http://{domain}/'
  sitemap = sitemap_tree_for_homepage(url)
  urls = {page.url for page in sitemap.all_pages()}
  urls = list(urls)
  if len(urls) > 0:
    with open("urls/" + domain+".txt", "w") as d:
      d.write("\n".join(urls))
  else:
    bad_domains.append(domain)

th = []
with open("domains.txt") as domains:
  for domain in domains:
    thread = threading.Thread(target=parse_sitemap, args=(domain, ))
    th.append(thread)
    thread.start()

for t in th:
  t.join()

if len(bad_domains) > 0:
  with open("bad_domains.txt", "w") as bdmns:
    bdmns.write("\n".join(bad_domains))
