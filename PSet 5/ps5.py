# 6.0001/6.00 Problem Set 5 - RSS Feed Filter

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        punctuation = list(string.punctuation)
        simple_text = ''
        for symbol in text:
            if symbol in punctuation:
                simple_text += ' '
            else:
                simple_text += symbol
        text = ' '.join(simple_text.split()) + ' '
        return (self.phrase + ' ') in text.lower()

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)

    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

class TimeTrigger(Trigger):
    def __init__(self, date_string):
        format = "%d %b %Y %H:%M:%S"
        self.trigger_time = datetime.strptime(date_string, format)

class BeforeTrigger(TimeTrigger):
    def __init__(self, date_string):
        TimeTrigger.__init__(self, date_string)

    def evaluate(self, story):
        story_time = story.get_pubdate().replace(tzinfo = pytz.timezone("EST"))
        return story_time < self.trigger_time.replace(tzinfo =
                                                      pytz.timezone("EST"))

class AfterTrigger(TimeTrigger):
    def __init__(self, date_string):
        TimeTrigger.__init__(self, date_string)

    def evaluate(self, story):
        story_time = story.get_pubdate().replace(tzinfo = pytz.timezone("EST"))
        return story_time > self.trigger_time.replace(tzinfo =
                                                      pytz.timezone("EST"))

# COMPOSITE TRIGGERS

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two

    def evaluate(self, story):
        return self.trigger_one.evaluate(story) and \
               self.trigger_two.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger_one, trigger_two):
        self.trigger_one = trigger_one
        self.trigger_two = trigger_two

    def evaluate(self, story):
        return self.trigger_one.evaluate(story) or \
               self.trigger_two.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    result = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                result.append(story)
    return result

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)
    triggers_names = {"TITLE": TitleTrigger, "DESCRIPTION": DescriptionTrigger,
                      "AFTER": AfterTrigger, "BEFORE": BeforeTrigger,
                      "NOT": NotTrigger, "AND": AndTrigger, "OR": OrTrigger}
    triggers_dict = {}
    triggers_list = []
    for line in lines:
        line = line.split(',')
        if (line[1] not in ["AND", "OR"]) and line[0] != "ADD":
            triggers_dict[line[0]] = triggers_names[line[1]](line[2])
        elif line[1] in ["AND", "OR"]:
            triggers_dict[line[0]] = \
                triggers_names[line[1]](triggers_dict[line[2]],
                                             triggers_dict[line[3]])
        elif line[0] == "ADD":
            for tr in range(1,len(line)):
                triggers_list.append(triggers_dict[line[tr]])
    return triggers_list



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:

        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end = ' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

