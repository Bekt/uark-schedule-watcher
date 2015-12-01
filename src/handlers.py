import json
import logging
import re
import webapp2
from models import Watcher

EMAIL_RE = re.compile(r'[^@]+@[^@]+\.[^@]+')

active_terms = [{'code': t[0], 'name': t[1]}
                for t in [
                    (1161, 'January Intersession 2016'),
                    (1163, 'Spring 2016'),
                    ]]


class AppHandler(webapp2.RequestHandler):

    def watch(self):
        req = json.loads(self.request.body)
        email = str(req.get('email', ''))
        class_num = str(req.get('course', ''))
        term = str(req.get('term', ''))
        if (EMAIL_RE.match(email) is None or
                not email.endswith('uark.edu')):
            logging.warning('Email invalid: {}'.format(email))
            self.write_json({'message': 'Invalid @uark email.'}, 400)
            return
        if (not class_num.isdigit()
                or int(class_num) < 1 or int(class_num) > 100000):
            logging.warning('Course number invalid: {}'.format(class_num))
            self.write_json({'message': 'Invalid course number.'}, 400)
            return
        if (not term.isdigit()
                or not any(t['code'] == int(term) for t in active_terms)):
            logging.warning('Term code not invalid: {}'.format(term))
            self.write_json({'message': 'Invalid term number.'}, 400)
            return
        watcher = Watcher(email=email.lower(),
                          class_num=int(class_num), strm=int(term))
        watcher.put()
        self.write_json()

    def terms(self):
        self.write_json(active_terms)

    def write_json(self, response={}, status=200):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(status)
        self.response.out.write(json.dumps(response))


app = webapp2.WSGIApplication([
    webapp2.Route(r'/cron/check', methods=['GET'],
                  handler='cron.CronHandler:check'),
    webapp2.Route(r'/cron/process', methods=['POST'],
                  handler='cron.CronHandler:process'),
    webapp2.Route(r'/watch', methods=['POST'],
                  handler='handlers.AppHandler:watch'),
    webapp2.Route(r'/terms', methods=['GET'],
                  handler='handlers.AppHandler:terms'),
])
