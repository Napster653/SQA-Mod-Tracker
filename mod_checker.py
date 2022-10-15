import requests
import re
import datetime

URL_FIXED_PART = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
MODLIST_FILE_NAME = 'modlist.cfg'
COMMENT_CHARACTER = '#'
REGEX_DATE_HTML = '(?:detailsStatsContainerRight[\S\s]+?\=[\S\s]+?\=[\S\s]+?\=[\S\s]+?\>)([^\<]+)'


def parse_steam_time(str_date):
    match_result = re.search('[0-9]{4}', str_date)

    if match_result is None:  # Date formatted as 'DD MMM @ hh:mmAP
        date_time_obj = datetime.datetime.strptime(str_date, '%d %b @ %I:%M%p')
        date_time_obj = date_time_obj.replace(year=datetime.datetime.now().year)
    else:  # Date formatted as 'DD MMM, YYYY @ hh:mmAP
        date_time_obj = datetime.datetime.strptime(str_date, '%d %b, %Y @ %I:%M%p')

    date_time_obj = date_time_obj + datetime.timedelta(hours=9)
    # print('Date: ', date_time_obj)
    return date_time_obj


modlist_file = open(MODLIST_FILE_NAME, 'r')
lines = modlist_file.readlines()

for line in lines:
    mod_id = line.partition(COMMENT_CHARACTER)[0].strip()
    mod_comment = line.partition(COMMENT_CHARACTER)[2].strip()
    url_full = URL_FIXED_PART + mod_id
    # print(mod_id, ": ", url_full)
    page = requests.get(url_full)
    str_date = re.search(REGEX_DATE_HTML, page.text).group(1)
    # print(str_date)
    last_update_date = parse_steam_time(str_date)
    current_date = datetime.datetime.now()
    delta = current_date - last_update_date
    if delta.days <= 7:
        print('Mod ', mod_comment, " (", mod_id, ") updated on ", last_update_date.isoformat())
