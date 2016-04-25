import datetime as dt
import get_auth
import pynder
import time

FB_ID = '100000178479403'

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
TIME_DIFFERENCE_FROM_UTC = 60 * 60 * 7


def convert_time(utc_time):
	seconds = time.mktime(dt.datetime.strptime(utc_time[:-1], TIME_FORMAT).timetuple())
	seconds -= TIME_DIFFERENCE_FROM_UTC
	return dt.datetime.fromtimestamp(int(seconds))


def filter_matches(matches):
	return [match for match in matches if match.user is not None]


def find_people_named(matches, name):
	people = []
	for match in matches:
		if match.user.name == name:
			people.append(match)

	return people


def match_with_all(session):
	swiped = []
	swiped_ids = set()
	queue = session.nearby_users()

	while len(queue) != 0:
		for girl in queue:
			if girl.id not in swiped_ids:
				try:
					girl.like()
					swiped.append(girl)
					swiped_ids.add(girl.id)
				except:
					continue

		queue = session.nearby_users()

	return swiped


if __name__ == '__main__':
	session = pynder.Session(FB_ID, get_auth.get_auth_token())

	matches = match_with_all(session)
	print len(matches)
	print matches
