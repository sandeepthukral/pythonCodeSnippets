import re
import logging


## This script is targeted to a specific whatsapp group
## The admin changes the subject whenever its the birthday or 
## marriage anniversary of a member of the group
## This script tries to identify the complete set of these events
## using an extract of the chat transcript that covers one year of chats

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

FILE = "whatsapp-ThukralFamily.txt"
REGEXP_BASIC = re.compile('^(.*),\s(.*)\s-\s(.*)')
REGEXP_SUBJECT_CHANGE = re.compile('^(.*),\s(.*)\s-\s(.*)( changed the subject to )(.*)')
REGEXP_THUKRAL = re.compile(r'.*Thukral|FAMILY|T\sH\sU\sK\sR\sA\sL.*', re.I)


def read_file_into_list():
    temp_list = []
    with open(FILE) as fileHandler:
        for index, line in enumerate(fileHandler.readlines()):
            searches = REGEXP_BASIC.findall(line)
            if searches:
                temp_list.append([i.decode('unicode_escape').encode('ascii', 'ignore') for i in list(searches[0])])
    return temp_list


def getAllRecords():
    temp_list = []
    with open(FILE) as fileHandler:
        for index, line in enumerate(fileHandler.readlines()):
            searches = REGEXP_SUBJECT_CHANGE.findall(line)
            if searches:
                if not REGEXP_THUKRAL.findall(searches[0][4]):
                    print("{} {} {}".format(searches[0][0], searches[0][1], searches[0][4].decode('unicode_escape').encode('ascii','ignore')))
                else:
                    logging.log(logging.DEBUG, "Skiping subject {}".format(searches[0][4]))
            temp_list.append((line))
    return temp_list


def main():
    all_lines = getAllRecords()


if __name__ == "__main__":
    main()
