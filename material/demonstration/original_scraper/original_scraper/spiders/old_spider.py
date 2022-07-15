import scrapy
from datetime import datetime
from scrapy.http import FormRequest, Request
from scrapy.utils.response import open_in_browser
from time import strptime
from json import dump

class Scraper(scrapy.Spider):

    name = 'time'
    start_urls = ['https://timetable.ul.ie/Login.aspx?ReturnUrl=%2fStudentTimetable.aspx']
    timetable = {}

    def __init__(self, student_id='18238831', pwd='Monday123'): # Input your ID number and password here to see orginal implementation
        self.timetable['class'] = []
        self.timetable['misc'] = {
            'id': '',
            'email': '',
            'pwd': '',
            'year': 0,
            'date_time': datetime.now().strftime('%d-%m-%y %H:%M')
        }
        self.timetable['misc']['id'] = student_id
        self.timetable['misc']['email'] = student_id+'@studentmail.ul.ie'
        self.timetable['misc']['pwd'] = pwd
        self.classes = []


    def parse(self, response):
        token = response.css('#__EVENTVALIDATION::attr(value)').extract_first()
        return FormRequest.from_response(response, formdata={"__EVENTVALIDATION": token, "TextBox_UserName":self.timetable['misc']['id'], "TextBox_Password":self.timetable['misc']['pwd']}, callback=self.LoggedIn)

    def LoggedIn(self, response):
        self.timetable['misc']['pwd'] = ''
        student_timetable_link = response.xpath('//*[@id="MainContent_StudentTile"]/a/@href').get()
        return response.follow(student_timetable_link, callback=self.GetTimetable)

    def GetTimetable(self, response):
        table = response.css('#MainContent_StudentTimetableGridView')
        days = [0, 1, 2, 3, 4, 5]
        rows = response.css('html body form#ctl01 div.container.body-content div.Grid div table#MainContent_StudentTimetableGridView.cssgridview.table-responsive tbody tr') # ~~~~~~~~~ Point the bot the table grid 
        print(rows)
        for row in rows[1:]:
            cells = row.xpath('td') #~~~~~ Use the table selector object to shortent the css path / xpath
            print(cells)
            day = 0
            for cell in cells:
                data = cell.xpath('text()').getall()
                print(data)
                # ['09:00 - 11:00', 'EE4216 - LAB - 2B', ' HAYES (ECE) MARTIN DR', 'Wks:4,8,13']
                for c in data:
                    if(c == ' '):
                        data.remove(c)
                    elif(c==r'\xa0'):
                        break
        #
                if(data == []):
                    continue
        #
                print("data: ", data)
                start_index = 0
                for d in data:
                    start_index += 1
                    if(TimeCheck(d)):
                        subdata = [d]
                        for elem in data[start_index:]:
                            print('elem: ', elem)
                            if(TimeCheck(elem)):
                                break
                            else:
                                subdata.append(elem)
                        
                        print("subdata: ", subdata)
                        new_class = ProcessClassData(subdata, days[day])
                        print('processed: ', new_class)
                        self.classes.append(new_class)
        
                day+=1

        return self.classes

    def closed(self, response):
        filename = r'output.json'
        with open(filename, 'w+') as db:
            dump(self.classes, db)
        pass

def TimeCheck(input):
    try:
        times = input.split('-')
        start_time = times[0].strip()
        end_time = times[1].strip()
        strptime(start_time, '%H:%M')
        strptime(end_time, '%H:%M')
        return True
    except ValueError:
        return False
    except IndexError:
        return False

def ProcessClassData(class_data, day):
    new_class = {
        'day': day,
        'professor': 'Null',
        'module': 'Null',
        'group': 'Null',
        'delivery': 'Null',
        'location': 'Null',
        'active_weeks': [],
        'start_time': '00:00',
        'end_time': '00:00'
    }
    #
    times = class_data[0].split('-')
    start_time = times[0].strip()
    end_time = times[1].strip()
    #
    class_desc = class_data[1].split('-')
    module = class_desc[0].strip()
    delivery = class_desc[1].strip()
    #
    try:
        group = class_desc[2].strip()
        new_class['group'] = group
    except IndexError as e:
        pass
    #
    try:
        professor = 'Unknown'
        location = ''
        if(len(class_data) < 5):
            # data missing
            unknown_data = class_data[-2].strip()
            location = unknown_data
            professor = unknown_data
        else:
            location = class_data[-2].strip()
            professor = class_data[2].strip()
        new_class['professor'] = professor
        new_class['location'] = location
    except IndexError as e:
        pass
    #
    active_weeks = class_data[-1].replace('Wks:', '').strip()
    active_weeks = active_weeks.split(',')
    #
    new_class['day'] = day
    new_class['start_time'] = start_time
    new_class['end_time'] = end_time
    new_class['module'] = module
    new_class['delivery'] = delivery
    new_class['active_weeks'] = active_weeks
    #           
    return new_class