from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat

from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number

#import magic, os
from pathlib import Path

def validate_possible_number(phone, country=None):
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code='invalid'
        )
    return phone_number


def max_filesize(file_, file_size= 1):
    MEGABYTE_LIMIT = file_size
    filesize = file_.size
    if filesize > MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError("file size should be maximum {0} MB".format( MEGABYTE_LIMIT ))

@deconstructible
class FileValidator(object):
    error_messages = {
        'max_size': ("Ensure this file size is not greater than %(max_size)s."
                  " Your file size is %(size)s."),
        'min_size': ("Ensure this file size is not less than %(min_size)s. "
                  "Your file size is %(size)s."),
        'content_type': "Files of type %(content_type)s are not supported.",
        'allowed_extensions': _( "File extension “%(extension)s” is not allowed. " "Allowed extensions are: %(allowed_extensions)s." ),
    }

    def __init__(self, max_size=None, min_size=None, content_types=(), allowed_extensions=None,):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        self.allowed_extensions = allowed_extensions

    def __call__(self, data):
        if self.max_size is not None and data.size > self.max_size:
            params = {
                'max_size': filesizeformat(self.max_size), 
                'size': filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages['max_size'],
                                   'max_size', params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                'min_size': filesizeformat(self.min_size),
                'size': filesizeformat(data.size)
            }
            raise ValidationError(self.error_messages['min_size'], 
                                   'min_size', params)

        if self.content_types:
            content_type = magic.from_buffer(data.read(), mime=True)
            data.seek(0)

            if content_type not in self.content_types:
                params = { 'content_type': content_type }
                raise ValidationError(self.error_messages['content_type'],
                                   'content_type', params)
        
        if self.allowed_extensions:
            extension = Path(data.name).suffix[1:].lower()
            if (
                self.allowed_extensions is not None
                and extension not in self.allowed_extensions
            ):
                raise ValidationError(
                    self.error_messages['allowed_extensions'],
                    params={
                        "extension": extension,
                        "allowed_extensions": ", ".join(self.allowed_extensions),
                        "value": data,
                    },
                )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.max_size == other.max_size and
            self.min_size == other.min_size and
            self.content_types == other.content_types and
            self.allowed_extensions == other.allowed_extensions
        )