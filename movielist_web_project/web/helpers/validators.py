from django.core.exceptions import ValidationError
import re

from django.utils.deconstruct import deconstructible

USERNAME_ONLY_LETTERS_NUMBERS_AND_UNDERSCORE_ERROR_MESSAGE = \
    'Username can contains only letters, numbers, and underscore.'

USERNAME_ONLY_LETTERS_ERROR_MESSAGE = 'First name can only contain letters!'


def validate_only_letters_numbers_and_underscore(value):
    is_valid = re.match(r'^[a-zA-Z0-9_]*$', value)

    if not is_valid:
        raise ValidationError(USERNAME_ONLY_LETTERS_NUMBERS_AND_UNDERSCORE_ERROR_MESSAGE)


def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError(USERNAME_ONLY_LETTERS_ERROR_MESSAGE)


@deconstructible
class MaxFileSizeInMbValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.__megabytes_to_bytes(self.max_size):
            raise ValidationError(self.__get_exception_message())

    @staticmethod
    def __megabytes_to_bytes(value):
        return value * 1024 * 1024

    def __get_exception_message(self):
        return f'Max file size is {self.max_size:.2f} MB'
