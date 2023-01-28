import datetime

def to_global_mobile(mobile, countory_code=81):
    if mobile.startswith('0'):
        mobile = mobile[1:]
    return '+' + str(countory_code) + mobile

def get_logfile_name() -> str:
    date = datetime.date.today().strftime("%Y-%m-%d")
    filename = "logs/"+date+".log";

    return filename