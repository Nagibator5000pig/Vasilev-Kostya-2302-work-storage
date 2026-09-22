from string import ascii_lowercase, digits
class CardCheck:
    CHARS_FOR_NAME = ascii_lowercase.upper() + digits
    @staticmethod
    def check_card_number(number):
        if len(number) != 19 or number[4] != '-' or number[9] != '-' or number[14] != '-':
            return False
        digits_only = number.replace('-', '')
        if not digits_only.isdigit():
            return False
        return True

    @classmethod
    def check_name(cls, name):
        words = name.split()
        if len(words) != 2:
            return False
        for w in words:
            if not all(c in cls.CHARS_FOR_NAME for c in w):
                return False
        return True

is_number = CardCheck.check_card_number("1234-5678-9012-0000")
is_name = CardCheck.check_name("IVAN IVANOV")

print(f'Номер карты: {is_number} \nИмя и фамилия: {is_name}')
