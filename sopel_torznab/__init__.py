# coding=utf8
"""sopel-torznab

Search a torznab-compatible torrent indexer from IRC with Sopel.
"""
from __future__ import unicode_literals, absolute_import, division, print_function
from sopel import module
import requests
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.tools import SopelMemory
import xml.etree.ElementTree as ET

class TorznabSection(StaticSection):
    endpoint = ValidatedAttribute('endpoint', str)
    apikey = ValidatedAttribute('apikey', str)
    lim_res = ValidatedAttribute('lim_res', int, default=5)

def setup(bot):
    bot.config.define_section('torznab', TorznabSection)

def configure(config):
    config.define_section('torznab', TorznabSection, validate=False)
    config.torznab.configure_setting('endpoint', 'What is the torznab endpoint to use?', default='')
    config.torznab.configure_setting('apikey', 'What is the torznab API key to use?')
    config.torznab.configure_setting('lim_res', 'What is the maximum number of results the search should return ?', default=5)

def format_bytes(size):
    size = int(size)
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(size).ljust(6)+power_labels[n]+'B'

@module.commands('torznab-search', 'tz-s')
@module.example('.tz-s Manjaro+iso')
def torznab_search(bot, trigger):
    """Search torrent indexer(s) using a torznab API."""
    bot.say('Searching torznab API for '+trigger.group(2)+ '...')
    url = bot.config.torznab.endpoint + 'api?apikey=' + bot.config.torznab.apikey + '&t=search&cat=&q=' + trigger.group(2)
    r = requests.get(url)
    #print(r.text)
    root = ET.fromstring(r.text).find('channel')
    res_list = []
    i = 0
    for item in root.findall('item'):
        title = item.find('title').text
        date = item.find('pubDate').text
        link = item.find('link').text
        size = format_bytes(item.find('size').text)
        comments = item.find('comments').text
        res_list.append([title, date, link, size, comments])
        bot.say('['+str(i)+'] '+title)
        #bot.say('['+str(i)+'] Title: '+title)
        #bot.say('Link: '+link)
        i += 1
        if i >= bot.config.torznab.lim_res:
            break
    if 'torznab_result_list' not in bot.memory:
        bot.memory['torznab_result_list'] = SopelMemory()
    bot.memory['torznab_result_list'][trigger.sender] = res_list
    bot.say('End of search.')
    

@module.commands('torznab-info', 'tz-i')
@module.example('.tz-i 3')
def torznab_info(bot, trigger):
    """Give info about a search result from a torznab API."""
    if 'torznab_result_list' not in bot.memory:
        bot.say('Do a torznab search first.')
        return
    if not trigger.group(2).isdigit():
        bot.say('Please give the number of a search result.')
        return
    res_list = bot.memory['torznab_result_list'][trigger.sender]
    title, date, link, size, comments = res_list[int(trigger.group(2))]
    bot.say('Title: '+title)
    bot.say('Date: '+date)
    bot.say('Size: '+size)
    bot.say('Comments: '+comments)
    bot.say('Link: '+link)
from sopel import module
import requests
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.tools import SopelMemory
import xml.etree.ElementTree as ET

class TorznabSection(StaticSection):
    endpoint = ValidatedAttribute('endpoint', str)
    apikey = ValidatedAttribute('apikey', str)
    lim_res = ValidatedAttribute('lim_res', int, default=5)

def setup(bot):
    bot.config.define_section('torznab', TorznabSection)

def configure(config):
    config.define_section('torznab', TorznabSection, validate=False)
    config.torznab.configure_setting('endpoint', 'What is the torznab endpoint to use?', default='')
    config.torznab.configure_setting('apikey', 'What is the torznab API key to use?')
    config.torznab.configure_setting('lim_res', 'What is the maximum number of results the search should return ?', default=5)

def format_bytes(size):
    size = int(size)
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(size).ljust(6)+power_labels[n]+'B'

@module.commands('torznab-search', 'tz-s')
@module.example('.tz-s Manjaro+iso')
def torznab_search(bot, trigger):
    """Search torrent indexer(s) using a torznab API."""
    bot.say('Searching torznab API for '+trigger.group(2)+ '...')
    url = bot.config.torznab.endpoint + 'api?apikey=' + bot.config.torznab.apikey + '&t=search&cat=&q=' + trigger.group(2)
    r = requests.get(url)
    #print(r.text)
    root = ET.fromstring(r.text).find('channel')
    res_list = []
    i = 0
    for item in root.findall('item'):
        title = item.find('title').text
        date = item.find('pubDate').text
        link = item.find('link').text
        size = format_bytes(item.find('size').text)
        comments = item.find('comments').text
        res_list.append([title, date, link, size, comments])
        bot.say('['+str(i)+'] '+title)
        #bot.say('['+str(i)+'] Title: '+title)
        #bot.say('Link: '+link)
        i += 1
        if i >= bot.config.torznab.lim_res:
            break
    if 'torznab_result_list' not in bot.memory:
        bot.memory['torznab_result_list'] = SopelMemory()
    bot.memory['torznab_result_list'][trigger.sender] = res_list
    bot.say('End of search.')
    

@module.commands('torznab-info', 'tz-i')
@module.example('.tz-i 3')
def torznab_info(bot, trigger):
    """Give info about a search result from a torznab API."""
    if 'torznab_result_list' not in bot.memory:
        bot.say('Do a torznab search first.')
        return
    if not trigger.group(2).isdigit():
        bot.say('Please give the number of a search result.')
        return
    res_list = bot.memory['torznab_result_list'][trigger.sender]
    title, date, link, size, comments = res_list[int(trigger.group(2))]
    bot.say('Title: '+title)
    bot.say('Date: '+date)
    bot.say('Size: '+size)
    bot.say('Comments: '+comments)
    bot.say('Link: '+link)
