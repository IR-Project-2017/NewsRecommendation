# Run this file first to scrape speficied subreddits

import praw
import datetime
import time
import random

# File to save to
post_file_path = "post_file.txt"
post_file = open(post_file_path, 'a')

# List of all subreddits we want to scrape
subreddits = ["worldnews", "China", "Africa", "Australia", "unitedKingdom", "UpliftingNews", "Economics", "soccer", "baseball"]
age_groups = ["10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
# Define date range to crawl, Year-Month-Day
datestart = datetime.date(2017, 4, 1)
dateend = datetime.date(2017, 5, 4)

ages = {group: random.randint(0, 100) for group in age_groups}
print(",".join(['%s:%s' % (key, value) for (key, value) in ages.items()]))

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
    # Convert dates to Unix time
    udatestart = time.mktime(datestart.timetuple())
    udateend = time.mktime(dateend.timetuple())
    print("Started scraping subreddit: " + subreddit)

    # Specify submissions from specified date
    submissions = reddit.subreddit(subreddit).submissions(udatestart, udateend)
    scraped_subs = 0
    # Get and Write all submissions to file, Format is "title \t url \t doc_id \t date \n", Wait 5 seconds if any server errors.
    try:
        for submission in submissions:
            # If submission is a "self-post", ignore it.
            if submission.is_self:
                continue
            # Stop scraping from this date if we have already done 300
            # if scraped_subs > 10000:
            #     break
            title = submission.title.encode('ascii', "ignore").decode("ascii")
            url = submission.url.encode('ascii', "ignore").decode("ascii")
            doc_id = submission.id.encode('ascii', "ignore").decode("ascii")
            post_date = datetime.datetime.fromtimestamp(int(submission.created)).strftime("%Y-%m-%d")
            # TODO Still problem with a couple of subs line breaking
            # if not any(c.isnumeric() for c in post_date) or not any(c.isalpha() for c in doc_id) or not any(c.isalpha() for c in url) or not any(c.isalpha() for c in title):
            #     print("Skipping title: " + title)
            #     continue
            post_file.write(title + "\t" + url + "\t" + doc_id + "\t" + post_date + "\t")
            ages = {group: random.randint(0, 100) for group in age_groups}
            post_file.write(",".join(['%s:%s' % (key, value) for (key, value) in ages.items()]))
            post_file.write("\t" + subreddit + "\n")
            scraped_subs += 1
    except Exception:
        print("HTTP error, waiting 5 seconds")
        time.sleep(5)
        continue

    print("Done scraping subreddit: " + subreddit)


post_file.close()
