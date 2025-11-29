from datetime import datetime, date
import random
import string


def parse_deadline(deadline: str) -> date:
    """
    Parse a deadline string in format YYYY/MM/DD.
    """
    try:
        parsed = datetime.strptime(deadline, "%Y/%m/%d").date()
        return parsed
    except ValueError:
        raise ValueError('inavlid deadline format')
    

def generate_random_string(length:int, digits:bool=False, lower:bool=False, upper:bool=False):
    if digits or lower or upper:
        temp = str()
        if digits:
            temp += string.digits
        if lower:
            temp += string.ascii_lowercase
        if upper:
            temp += string.ascii_uppercase
        result = ''.join(random.choices(temp, k=length))
    else:
        result = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))
    if result.startswith('0'):
        return generate_random_string(length=length, digits=digits, lower=lower, upper=upper)
    return result


def generate_random_id(length:int = 6) -> int:
    return int(generate_random_string(length=length, digits=True))
