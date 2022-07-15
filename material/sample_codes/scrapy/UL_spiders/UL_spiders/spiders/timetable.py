import scrapy

class TimetableSpider(scrapy.Spider):
    name = 'timetable'
    allowed_domains = ['timetable.ul.ie']
    start_urls = ['http://timetable.ul.ie/CourseTimetable.aspx']

    def parse(self, response):
        scrapy.utils.response.open_in_browser(response)
        pass
