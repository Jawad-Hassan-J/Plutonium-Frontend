
# test function
def add_five(user_input_request=None, user_input_file=None):
    if str(user_input_request).isdigit():
        return int(user_input_request) + 5
    return "error"


