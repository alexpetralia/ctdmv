from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

from django.core.management.base import BaseCommand

from ctdmv.models import WaitEntry


URL = 'https://www.dmvselfservice.ct.gov/NemoService.aspx'

def extract_wait_times(branch, data):
    """Accepts a payload, POSTs to the resource endpoint and returns a table"""
    data.update({data['_EVENTTARGET']: branch})
    response = requests.post(URL, data=data)
    soup = BeautifulSoup(response.content, 'html5lib')
    table = soup.select('table[id*="WaitTimes"]')[0]
    df = pd.read_html(str(table))[0]
    return df

def scrape_branches() -> list:
    """Scrapes list of branches & builds required payload from website"""
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html5lib')
    form = soup.find(id='aspnetForm')
    branches = [
        b.attrs['value'] for b in form.find('select').findAll('option')[1:]
    ]
    target = form.find('select').attrs['name']

    # Build payload
    data = {i.attrs['name']: i.attrs['value'] for i in form.findAll('input')}
    data.update(
        {'_EVENTTARGET': target, '_LASTFOCUS': '', '_EVENTARGUMENT': ''}
    )

    # Iterate over each branch
    dfs = [extract_wait_times(branch, data) for branch in branches]
    return list(zip(branches, dfs))


def write_to_db(data) -> None:
    """Accepts a tuple of (branch, pd.DataFrame) and writes each row into
    the database as a WaitEntry object"""
    for branch, df in data:
        for _, row in df.drop(0).iterrows():
            WaitEntry.factory(
                branch=branch,
                service=row[0],
                wait_time_str=row[1],
                num_waiting=row[2],
            )


class Command(BaseCommand):
    help = "Scrape all DMV entries"""

    def handle(self, *args, **kwargs):
        write_to_db(scrape_branches())

        # Heroku Scheduler only works at resolution of 10 minutes,
        # so we want to run _twice_ (i.e. 5 mins) during each interval
        time.sleep(5 * 60)
        write_to_db(scrape_branches())


# Schedule (daytime only)
# Catch errors (if no data, skip snapshot)
# Email errors
