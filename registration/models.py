import binascii
import os

from django.conf import settings
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
import zarinpal.functions as zarinpal


class Payment(models.Model):
    merchant_id = models.CharField(verbose_name=_('Merchant ID'),
                                   max_length=50,
                                   null=False,
                                   blank=False)
    amount = models.IntegerField(verbose_name=_('Amount'),
                                 null=False)
    description = models.CharField(verbose_name=_('Description'),
                                   max_length=100,
                                   null=False,
                                   blank=True)
    callback_url = models.CharField(verbose_name=_('Callback URL'),
                                    max_length=100,
                                    null=False,
                                    blank=True)
    active = models.BooleanField(verbose_name=_('Is Active?'),
                                 null=False,
                                 default=False)


class Participant(models.Model):
    first_name = models.CharField(verbose_name=_('First Name'),
                                  max_length=100,
                                  blank=False,
                                  null=False)
    last_name = models.CharField(verbose_name=_('Last Name'),
                                 max_length=100,
                                 blank=False,
                                 null=False)
    national_id = models.CharField(verbose_name=_('National ID No.'),
                                   max_length=10,
                                   blank=False,
                                   null=False,
                                   unique=True,
                                   validators=[MinLengthValidator(10)])
    email = models.EmailField(verbose_name=_('Email'))

    def mail_password(self, password=None):
        if not password:
            password = self.team.password
        send_mail(_('Farzcode Contest'),
                  "سلام :)\n برای شرکت در مسابقه‌ی فرزکد از این Username و Password استفاده کنید.\n\nUsername: {}\nPassword: {}\n"
                  "\nلطفن به فارسی یا انگلیسی بودن ارقام دقّت کنید.".format(
                      self.national_id, password),
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  fail_silently=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Team(models.Model):
    GRADE_A = 'A'
    GRADE_B = 'B'
    GRADE_CHOICES = (
        (GRADE_A, _('A')),
        (GRADE_B, _('B')),
    )
    title = models.CharField(verbose_name=_('Team Name'),
                             max_length=50,
                             blank=False,
                             null=False,
                             unique=True)
    grade = models.CharField(verbose_name=_('Grade'),
                             max_length=1,
                             choices=GRADE_CHOICES,
                             default=GRADE_A,
                             blank=False,
                             null=False)
    transaction = models.CharField(verbose_name=_('Authentication Serial'),
                                   max_length=100,
                                   null=False,
                                   blank=False)
    first_member = models.ForeignKey(Participant,
                                     related_name='teams_as_first_member',
                                     on_delete=models.CASCADE)
    second_member = models.ForeignKey(Participant,
                                      related_name='teams_as_second_member',
                                      on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,
                                verbose_name=_('Payment Type'),
                                on_delete=models.SET_NULL,
                                null=True,
                                default=None)
    password = models.CharField(verbose_name=_('password'),
                                max_length=50,
                                null=True,
                                blank=False)
    payment_party = models.BooleanField(verbose_name=_('Party in Payment?'),
                                        null=False,
                                        default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def payed(self):
        try:
            return zarinpal.verify(self) in [0, 1]
        except Exception as e:
            return True

    def gen_password(self, length=15, commit=True):
        password = binascii.hexlify(os.urandom(length)).decode('ascii')
        if len(password) > 50:
            raise Exception('generated password too long')
        self.password = password
        if commit:
            self.save()

    def mail_password(self):
        self.first_member.mail_password(password=self.password)
        self.second_member.mail_password(password=self.password)

    def save(self, *args, **kwargs):
        if not self.password:
            self.gen_password(commit=False)
        return super(Team, self).save(args, kwargs)

    def __str__(self):
        return self.title
