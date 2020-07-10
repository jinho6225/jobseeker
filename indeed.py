import requests
from bs4 import BeautifulSoup

LIMIT = 50


def extract_indeed_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find("div", {"class": "pagination"})
    if pagination is not None:
        links = pagination.find_all("a")
        pages = []
        for link in links[:-1]:
            pages.append(int(link.string))
        max_page = pages[-1]
    else:
        max_page = 1
    return max_page


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        "title": title,
        "company": company,
        "location": location,
        "link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_indeed_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page}")
        result = requests.get(f"{url}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs



def get_jobs_indeed(word, posted_date):
  if posted_date == "one_day":
    posted_date = 1
  elif posted_date == "one_week":
    posted_date = 7
  url = f"https://www.indeed.com/jobs?q={word}&l=Los%20Angeles%2C%20CA&radius=50&limit={LIMIT}&fromage={posted_date}"
  last_page = extract_indeed_pages(url)
  indeed_jobs = extract_indeed_jobs(last_page, url)
  return indeed_jobs
