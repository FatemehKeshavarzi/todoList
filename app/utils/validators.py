from datetime import date

def validate_deadline(deadline:date) -> bool:
    if deadline >= date.today():
        return True
    return False