#!/usr/bin/python
import browsercookie
import sys, mechanize, cookielib, tinder

def get_auth_token():
	# Browser
	br = mechanize.Browser()

	# Cookie Jar
	cookies = mechanize.CookieJar()
	br.set_cookiejar(browsercookie.chrome())

	# Browser options
	br.set_handle_equiv(True)
	br.set_handle_gzip(False)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	headers = [
	    ('host', 'www.facebook.com'),
	    ('method', 'GET'),
	    ('path', '/login.php?skip_api_login=1&api_key=464891386855067&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.0%2Fdialog%2Foauth%3Fredirect_uri%3Dhttps%253A%252F%252Fwww.facebook.com%252Fconnect%252Flogin_success.html%26scope%3Dbasic_info%252Cemail%252Cpublic_profile%252Cuser_about_me%252Cuser_activities%252Cuser_birthday%252Cuser_education_history%252Cuser_friends%252Cuser_interests%252Cuser_likes%252Cuser_location%252Cuser_photos%252Cuser_relationship_details%26response_type%3Dtoken%26client_id%3D464891386855067%26ret%3Dlogin&cancel_url=https%3A%2F%2Fwww.facebook.com%2Fconnect%2Flogin_success.html%3Ferror%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied%23_%3D_&display=page'),
	    ('scheme', 'https'),
	    ('version', 'HTTP/1.1'),
	    ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
	    ('accept-encoding', 'gzip, deflate, sdch'),
	    ('accept-language', 'en-US,en;q=0.8'),
	    ('cache-control', 'max-age=0'),
	    ('pragma', 'no-cache'),
	    ('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36'),
	]

	br.addheaders = headers
	br.open('https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token')

	current_url = br.response().geturl()
	access_token = current_url[current_url.index('access_token=') + 13 : current_url.index('&')]
	return access_token
