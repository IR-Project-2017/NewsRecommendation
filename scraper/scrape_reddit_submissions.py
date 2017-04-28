# Run this file first to scrape speficied subreddits

import praw
import datetime
import time

# File to save to
post_file_path = "post_file.txt"
post_file = open(post_file_path, 'a')

# List of all subreddits we want to scrape
subreddits = ["worldnews"]
# Define date range to crawl, Year-Month-Day
datestart = datetime.date(2017, 3, 26)
dateend = datetime.date(2017, 4, 27)

# Specify reddit bot, needs to be created at https://www.reddit.com/prefs/apps/
reddit = praw.Reddit(client_id='kiEkGfkxQ71Dpg',
                     client_secret='2wk6Gihtvtx3B8PyPJ8CLV9X23s',
                     user_agent='PrawScraper',
                     username='schoolstuff01',
                     password='kth123456')


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

# Iterate over each subreddit
for subreddit in subreddits:
    # Iterate over specified date range
    for date in daterange(datestart, dateend):

        print("Started scraping date: " + date.strftime("%Y-%m-%d"))

        # Convert dates to Unix time
        udatestart = time.mktime(datestart.timetuple())
        udateend = time.mktime(dateend.timetuple())

        # Specify submissions from specified date
        submissions = reddit.subreddit(subreddit).submissions(udatestart, udateend)

        # Get and Write all submissions to file, Format is "title \t url \t doc_id \t date \n", Wait 5 seconds if any server errors.
        try:
            for submission in submissions:
                title = submission.title.encode('ascii', "ignore").decode("ascii")
                url = submission.url.encode('ascii', "ignore").decode("ascii")
                doc_id = submission.id.encode('ascii', "ignore").decode("ascii")
                post_date = date.strftime("%Y-%m-%d")
                post_file.write(title + "\t" + url + "\t" + doc_id + "\t" + post_date + "\t" + subreddit + "\n")
        except Exception:
            print("HTTP error, waiting 5 seconds")
            time.sleep(5)
            continue

        print("Done scraping date: " + date.strftime("%Y-%m-%d"))


post_file.close()
