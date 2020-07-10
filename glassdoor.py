import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def extract_glassdoor_pages(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    max_pages = soup.find("div", {"class": "padVertSm"}).string
    max_pages = int(max_pages[max_pages.index("of")+2:])
    if max_pages is None:
        max_pages = 1
    return max_pages


def extract_glassdoor_jobs(last_page, posted_date):
  jobs = []
  for page in range(1, last_page+1):
      print(f"Scrapping page {page}")
      result = requests.get(f"https://www.glassdoor.com/Job/los-angeles-javascript-jobs-SRCH_IL.0,11_IC1146821_KO12,22_IP{page}.htm?fromAge={posted_date}&radius=100", headers=headers)
      soup = BeautifulSoup(result.text, 'html.parser')
      article = soup.find("article", {"class": "noPad"})
      ul = article.find("ul", {"class":"jlGrid hover"})
      results = ul.find_all("li", {"class":"react-job-listing"})
      for result in results:
          job = extract_job(result)
          jobs.append(job)
  return jobs


def extract_job(html):
    company = html.find("div", {"class": "jobContainer"}).find("div", {"class": "jobEmpolyerName"}).string
    link = html.find("div", {"class": "jobContainer"}).find("a")["href"]
    title = html.find("div", {"class": "jobContainer"}).find_all("a")[1].string
    location = html.find("div", {"class": "jobContainer"}).find("div", {"class": "empLoc"}).find("span").string

    return {
        "title": title,
        "company": company,
        "location": location,
        "link": link
    }

def get_jobs_glassdoor(serach_word, posted_date):
  if posted_date == "one_day":
    posted_date = 1
  elif posted_date == "one_week":
    posted_date = 7
  url = f"https://www.glassdoor.com/Job/los-angeles-{serach_word}-jobs-SRCH_IL.0,11_IC1146821_KO12,22_IP1.htm?fromAge={posted_date}&radius=100"
  last_page = extract_glassdoor_pages(url)
  indeed_jobs = extract_glassdoor_jobs(last_page, posted_date)
  return indeed_jobs
