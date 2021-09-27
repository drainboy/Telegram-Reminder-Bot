import json

PARTICIPANTS_FILENAME = "participants.json"
PASSED_BATON_FILENAME = "passed_baton.json"
PARTICIPANTS_LIST = []
PASSED_BATON_LIST = []


def init(filename, dict_list):
    """Initialize from file to dictionary"""
    with open(filename, 'r') as file:
        dictionary = json.load(file)
        for key, value in dictionary.items():
            dict_list.append({int(key): value})
    return dictionary


def update_file(filename, dict_list):
    """Update filename with given list"""
    output_dictionary = {}

    for dictionary in dict_list:
        output_dictionary.update(dictionary)

    with open(filename, 'w') as file:
        json.dump(output_dictionary, file, indent=4)


def add_to_list(chat_id, first_name, last_name, dict_list):
    """Add given user information to the dictionary list"""
    participant_dict = {chat_id: {"first_name": first_name, "last_name": last_name}}
    dict_list.append(participant_dict)
    print(dict_list)


def delete(chat_id, dict_list):
    """Remove user information from the dictionary list"""
    for index in range(len(dict_list)):
        dictionary = dict_list[index]
        if chat_id in dictionary:
            dict_list.pop(index)


def pass_baton(chat_id, dict_list, passed_baton_list):
    """Moves user information from the dictionary list to passed_baton_list if user is first place"""
    if chat_id in dict_list[0]:
        passed_baton_list.append(dict_list.pop(0))


def switch(chat_id, index):
    pass


def routine_order(dict_list, passed_baton_list):
    """Add all user information from passed_baton_list to dictionary list"""
    for each in passed_baton_list[::-1]:
        dict_list.insert(0, each)

    passed_baton_list.clear()
