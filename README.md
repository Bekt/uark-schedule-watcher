## UArk Schedule Watcher
**UArk Schedule Watcher** is designed to help students at the University of
Arkansas, Fayetteville with course sign-ups. Students no longer have to
check ISIS for course availability manually. The service notifies the
students whenever a course status changes from full/waitlist/closed to
open.

## Live
http://usw.bekt.net

![](https://cloud.githubusercontent.com/assets/1221480/5658631/a9b8d03a-96ca-11e4-8a14-6b7a54fce8e3.png)

## Development
### Requirements
* Google App Engine SDK for Python: https://cloud.google.com/appengine/downloads

### Running Locally
```bash
git clone git@github.com:Bekt/uark-schedule-watcher.git
cd uark-schedule-watcher
pip install -t lib/ -r requirements.txt

<path-to-gae-SDK>/dev_appserver.py .
```

The service should now be running at http://localhost:8080

## Architecture
The service runs on Google App Engine, and uses a couple of its key
features. It can easily support thousands and thousands of watchers
because of App Engine's Cron Service and Task Queue API. Below is a high overview:

1. Every N minutes, a [cron task](https://cloud.google.com/appengine/docs/python/config/cron) is scheduled.
2. The task kicks of a background job for each "active watcher" using the [Task Queue
API](https://cloud.google.com/appengine/docs/python/taskqueue/).
3. Each task queue job checks course availability, and sends out an email if the course status has changed to open.

## License
[The MIT License](http://opensource.org/licenses/MIT)
