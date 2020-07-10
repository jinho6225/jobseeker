from flask import Flask, render_template, request, redirect, send_file
from indeed import get_jobs_indeed
from glassdoor import get_jobs_glassdoor
from exporter import save_to_file

app = Flask("Hey")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/report_indeed")
def report_indeed():
  word = request.args.get("word")
  posted_date = request.args.get("posted_date")
  word = word.lower()
  jobs = get_jobs_indeed(word, posted_date)

  return render_template("report_indeed.html",
  word=word,
  posted_date=posted_date,
  resultNum=len(jobs),
  jobs=jobs
  )

@app.route("/report_glassdoor")
def report_glassdoor():
  search_word = request.args.get("search")
  posted_date = request.args.get("posted_date")
  search_word = search_word.lower()
  jobs = get_jobs_glassdoor(search_word, posted_date)

  return render_template("report_glassdoor.html",
  word=search_word,
  posted_date=posted_date,
  resultNum=len(jobs),
  jobs=jobs
  )

@app.route("/export_indeed")
def export1():
  try:
    word = request.args.get('word')
    posted_date = request.args.get("posted_date")
    if not word:
      raise Exception()
    jobs = get_jobs_indeed(word, posted_date)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

@app.route("/export_glassdoor")
def export2():
  try:
    word = request.args.get('word')
    posted_date = request.args.get("posted_date")
    if not word:
      raise Exception()
    jobs = get_jobs_glassdoor(word, posted_date)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file("jobs.csv")
  except:
    return redirect("/")

app.run()
