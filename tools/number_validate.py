def valida_num(answers):
    try:
        int(answers['threads'])
        int(answers['time'])
        return True
    except ValueError:
        return False
