import datetime
import logging
import typing
import zoneinfo


def to_global_mobile(mobile, countory_code=81):
    if mobile.startswith('0'):
        mobile = mobile[1:]
    return '+' + str(countory_code) + mobile

def get_logfile_name() -> str:
    date = datetime.date.today().strftime("%Y-%m-%d")
    filename = "logs/"+date+".log";

    return filename

def get_answers(questions: typing.Dict, answers: typing.List[str], logger):
    res = []
    
    for question, answer in zip(questions, answers):
        
        answer_id = list(filter(lambda item: item['answer_text'] == answer, question["options"]))
        
        if len(answer_id) == 0:
            logger.error(f"Invalid answer: {answer}")
        
        res.append(answer_id[0]["id"])
    
    return res

def get_time(*arg):
    return datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).timetuple()

def get_formatter():
    formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s | %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S +09:00",
    )
    formatter.converter = get_time
    
    return formatter