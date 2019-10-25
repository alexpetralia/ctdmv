# CT DMV Wait Times 🚗

### Description

I noticed the [CT DMV website](https://www.dmvselfservice.ct.gov/NemoService.aspx) offers wait time information but it doesn't do it in a time series format. This means we can only see a "snapshot" of wait times at the current moment, but can't evaluate any patterns over time. I built a simple app to store this wait time data over time, serve it over an API , and visualize it on a webapp.

.

### Tech stack

* Deployment: Heroku
* Data scraping: `requests` job every 5 minutes via Heroku Scheduler
* Backend: Python `django` serving REST APIs via djangorestframework
* Frontend: `Vue.js`, `Chart.js`

.

### API

The API is available using the following endpoints:

* `/api/wait_times/`

The raw wait time data, where each record represents a "wait time entry". A wait time entry is a particular wait time snapshot for a given branch and a given service service.

* `/api/wait_times/<monthly|weekly|daily>/`

The aggregated wait time data, where the frequencies available are `monthly`, `weekly` and `daily`. This returns mean wait times, or the number of people, waiting over a typical month (daily averages), a typical week (weekday averages), or a typical day (5-minute averages).

.

All API endpoints accept the following filters as GET parameters:

`weekday: int` (0: Monday, 7: Sunday)

`branch: str` (branch name, case insensitive contains)

`service: str` (service name, case insensitive contains)

`date_before: str` (subset data before, format: YYYY-MM-DD)

`date_after: str` (subset data after, format: YYYY-MM-DD)

.

Example query: `https://ctdmv.herokuapp.com/api/wait_times/monthly/?branch=bridgeport&service=registration transactions&date_after=2019-10-10&date_before=2019-10-24&weekday=3`

.

### Raw data

If you would like to download the raw data, you can query the API directly. There are two additional GET parameters you can use:

`format` (csv, json)

`page_size` (0 to 5,000)

.

Example query: `https://ctdmv.herokuapp.com/api/wait_times/?branch=danbury&service=dealer transactions&date_after=2019-10-10&date_before=2019-10-24&format=csv&page_size=100000`

(Note the final two parameters)

All timestamps are returned in UTC time (generally this is 4 or 5 hours before UTC time).

.

### License

This project is licensed under the terms of the MIT license. You can read more in the `LICENSE` file.
