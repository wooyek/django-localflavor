"""Belgium-specific Form helpers."""

from django.forms.fields import RegexField, Select
from django.utils.translation import ugettext_lazy as _

from localflavor.deprecation import DeprecatedPhoneNumberFormFieldMixin

from .be_provinces import PROVINCE_CHOICES
from .be_regions import REGION_CHOICES


class BEPostalCodeField(RegexField):
    """
    A form field that validates its input as a belgium postal code.

    Belgium postal code is a 4 digits string. The first digit indicates
    the province (except for the 3ddd numbers that are shared by the
    eastern part of Flemish Brabant and Limburg and the and 1ddd that
    are shared by the Brussels Capital Region, the western part of
    Flemish Brabant and Walloon Brabant)
    """

    default_error_messages = {
        'invalid': _(
            'Enter a valid postal code in the range and format 1XXX - 9XXX.'),
    }

    def __init__(self, *args, **kwargs):
        super(BEPostalCodeField, self).__init__(r'^[1-9]\d{3}$', *args, **kwargs)


class BEPhoneNumberField(RegexField, DeprecatedPhoneNumberFormFieldMixin):
    """
    A form field that validates its input as a belgium phone number.

    Landlines have a seven-digit subscriber number and a one-digit area code,
    while smaller cities have a six-digit subscriber number and a two-digit
    area code. Cell phones have a six-digit subscriber number and a two-digit
    area code preceeded by the number 4.
    0d ddd dd dd, 0d/ddd.dd.dd, 0d.ddd.dd.dd,
    0dddddddd - dialling a bigger city
    0dd dd dd dd, 0dd/dd.dd.dd, 0dd.dd.dd.dd,
    0dddddddd - dialling a smaller city
    04dd ddd dd dd, 04dd/ddd.dd.dd,
    04dd.ddd.dd.dd, 04ddddddddd - dialling a mobile number

    .. deprecated:: 1.4
        Use the django-phonenumber-field_ library instead.

    .. _django-phonenumber-field: https://github.com/stefanfoulis/django-phonenumber-field
    """

    default_error_messages = {
        'invalid': _('Enter a valid phone number in one of the formats '
                     '0x xxx xx xx, 0xx xx xx xx, 04xx xx xx xx, '
                     '0x/xxx.xx.xx, 0xx/xx.xx.xx, 04xx/xx.xx.xx, '
                     '0x.xxx.xx.xx, 0xx.xx.xx.xx, 04xx.xx.xx.xx, '
                     '0xxxxxxxx or 04xxxxxxxx.'),
    }

    def __init__(self, *args, **kwargs):
        super(BEPhoneNumberField, self).__init__(r'^[0]\d{1}[/. ]?'
                                                 r'\d{3}[. ]\d{2}[. ]?'
                                                 r'\d{2}$|^[0]\d{2}[/. ]?'
                                                 r'\d{2}[. ]?\d{2}[. ]?'
                                                 r'\d{2}$|^[0][4]\d{2}[/. ]?'
                                                 r'\d{2}[. ]?'
                                                 r'\d{2}[. ]?'
                                                 r'\d{2}$',
                                                 *args, **kwargs)


class BERegionSelect(Select):
    """A Select widget that uses a list of belgium regions as its choices."""

    def __init__(self, attrs=None):
        super(BERegionSelect, self).__init__(attrs, choices=REGION_CHOICES)


class BEProvinceSelect(Select):
    """A Select widget that uses a list of belgium provinces as its choices."""

    def __init__(self, attrs=None):
        super(BEProvinceSelect, self).__init__(attrs, choices=PROVINCE_CHOICES)
