import datetime


class SystemInfo:
    def __init__(self):
        pass

    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        if now.hour >= 12:
            hour = now.hour - 12
            return  hour
        else:
            hour = now.hour

        answer = 'The time now is {} {}'.format(hour, now.minute)
        return answer

    @staticmethod
    def get_date():
        now = datetime.datetime.now()
        day_num = now.day
        day_indx = now.weekday
        month_idx = now.month
        year = now.year
        month = ['January', 'February', 'March', 'April', 'May', "June",
                 'July', 'August', 'September',  'October', 'November', 'December']
        day = ['Monday', 'Tuesday', 'Wednesday',  'Thursday', 'Friday', 'Saturday', 'Sunday']
        ordinal_num = ['1st','2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
        '11th', '12th', '13th', '14th', '15th','16th', '17th', '18th', '19th', '20th',
        '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

        answer = 'Today is  {} {} {} of {}'.format(day.append(day_indx - 1),  month.append(month_idx),  day.append(day_num), year)

        return answer

    @staticmethod
    def get_year():
        now = datetime.datetime.now()
        answer = 'The year is {}'.format(now.year)
        return answer


print(SystemInfo.get_date())

