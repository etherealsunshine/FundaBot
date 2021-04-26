from asyncio.windows_events import NULL


def check_number(input):
    try:
        int(input)
        return True
    except ValueError:
        try:
            float(input)
            return True
        except ValueError:
            return False

def is_zero(input):
    return input == 0