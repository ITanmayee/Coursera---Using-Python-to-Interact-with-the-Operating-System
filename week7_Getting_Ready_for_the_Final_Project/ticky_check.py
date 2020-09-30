#!/usr/bin/env python3
import re,sys,os,operator

def check_message_type(pattern, log) :
    if re.search(pattern, log) is None :
        return False 
    return True

def error_search(log_file):
    error_message = {}
    error_pattern = r"ticky: ERROR ([\w ]*) "
    with open(log_file, mode='r',encoding='UTF-8') as file:
        for log in  file.readlines():
            if check_message_type(error_pattern, log):
                error = re.search(error_pattern, log)
                if error.group(1) not in error_message :
                    error_message[error.group(1)] = 1
                else :
                    error_message[error.group(1)] += 1
    file.close()
    sorted_error_messages = sorted(error_message.items(), key = operator.itemgetter(1), reverse=True)  
    return sorted_error_messages

def get_user_name(log) :
    details = log.strip().split()
    user_name = details[-1]
    return user_name[1:-1]

def user_statistics(log_file) :
    user_details = {}
    ticky_pattern, info_pattern, error_pattern = r"ticky", r"INFO", r"ERROR"
    with open(log_file, mode='r',encoding='UTF-8') as file:
        for log in  file.readlines():
            user_name = get_user_name(log)
            if  check_message_type(info_pattern, log):
                if user_name not in user_details :
                    user_details[user_name] = [1,0]
                else :
                    user_details[user_name][0] = user_details[user_name][0] + 1
            if  check_message_type(error_pattern, log):
                if user_name not in user_details :           
                    user_details[user_name] = [0,1]
                else :
                    user_details[user_name][1] = (user_details[user_name])[1] + 1
    file.close()
    sorted_user_details = sorted(user_details.items())
    return sorted_user_details


def write_error_messages(log_file) :
    error_messages =  error_search(log_file)
    with open( 'error_message.csv', 'w') as file:
         file.write("Error,Count" + "\n")
         for error_message in error_messages:
             file.write(error_message[0] + ',' + str(error_message[1]) + '\n')
    file.close()

def write_user_details(log_file) :
    user_details =  user_statistics(log_file)
    with open( 'user_statistics.csv', 'w') as file:
         file.write("Username,INFO,ERROR" + "\n")
         for user in user_details:
             file.write(user[0] + ',' + str(user[1][0]) + ',' + str(user[1][1]) + '\n')
    file.close()


if __name__ == "__main__":
    log_file = sys.argv[1]
    write_error_messages(log_file)
    write_user_details(log_file)


