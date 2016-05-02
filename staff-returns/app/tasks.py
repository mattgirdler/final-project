import calendar
from datetime import datetime


# TODO - Allow for multiple posts of the same project
def sort_monthly_projects(form_data):
    sorted_projects = {}
    form_data_dict = form_data.to_dict()
    num_rows = int((len(form_data_dict) / 2))
    for i in range(1, num_rows + 1):
        if form_data_dict['project_select_' + str(i)] == 'Select a Project':
            break;
        else:
            sorted_projects[form_data_dict['project_select_' + str(i)]] = form_data_dict['project_input_' + str(i)]
    return sorted_projects


def calculate_hours_required():
    days = [["Monday", 0]["Tuesday", 1]["Wednesday", 2]["Thursday", 3]["Friday", 4]["Saturday", 5]["Sunday": 6]]
    for day in days:
        print(day)
        print(len([1 for i in calendar.monthcalendar(datetime.now().year, datetime.now().month) if i[days[day]] != 0]))