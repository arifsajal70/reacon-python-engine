# Import documents
from app.documents.setting_document import Setting
from app.documents.currency_document import Currency
from app.documents.client_document import Client
from app.documents.admin_document import Admin

# Import Helpers
from app.helpers.dict import AttrDict

# Import Mongoengine Things
from mongoengine import Q

# Import Utils
from faker import Faker
import os
import bcrypt

settings = [
    # Site Information
    AttrDict(dict(field='site_name', value='Reacon Cash', type='str')),
    AttrDict(dict(field='site_email', value='info@reacon.cash', type='str')),

    # Referral Bonus Information
    AttrDict(dict(field='is_referral_on', value='True', type='bool')),
    AttrDict(dict(field='referral_generation', value='8', type='int'))
]

currencies = [
    AttrDict(dict(name='Bangladeshi Taka', short_code='BDT', symbol='tk', exchange_rate=0.00, default=False,
                  can_withdraw=False, can_pay=False, type='fiat')),
    AttrDict(dict(name='United States Dollar', short_code='USD', symbol='$', exchange_rate=0.00, default=True,
                  can_withdraw=False, can_pay=False, type='fiat')),
    AttrDict(dict(name='Ethereum', short_code='ETH', symbol='ETH', exchange_rate=0.00, default=False,
                  can_withdraw=False, can_pay=True, type='crypto')),
    AttrDict(dict(name='Bitcoin', short_code='BTC', symbol='BTC', exchange_rate=0.00, default=False,
                  can_withdraw=False, can_pay=True, type='crypto')),
]


def install_settings():
    for setting in settings:
        if not Setting.has_field(setting.field):
            Setting(
                field=setting.field,
                value=setting.value,
                type=setting.type
            ).save()
            print(f'Field => {setting.field} Value => {setting.value} Type => {setting.type}')
        else:
            setit = Setting.get_field(setting.field)
            if setit:
                setit.value = setting.value
                setit.save()
                print(f'Field => {setting.field} Value => {setting.value} Type => {setting.type}')


def install_referral_generation_settings():
    total_generation = Setting.get_field('referral_generation')

    Setting.objects(Q(field__istartswith='referer_limit_') | Q(field__istartswith='referer_type_') |
                    Q(field__istartswith='referer_amount_')).delete()

    for level in range(1, int(total_generation.value) + 1):
        if not Setting.has_field(f'ref_gen_bonus_limit_{level + 1}'):
            Setting(
                field=f'referer_limit_{level}',
                value='-1',
                type='int'
            ).save()
            Setting(
                field=f'referer_type_{level}',
                value='percent',
                type='str'
            ).save()
            Setting(
                field=f'referer_amount_{level}',
                value='5',
                type='float'
            ).save()
            print(f'Generation Bonus Created for Level => {level}')


def install_currencies():
    for currency in currencies:
        prev_cur = Currency.get_by_short_code(currency.short_code)
        if not prev_cur:
            Currency(
                name=currency.name,
                short_code=currency.short_code,
                symbol=currency.symbol,
                exchange_rate=currency.exchange_rate,
                default=currency.default,
                can_withdraw=currency.can_withdraw,
                can_pay=currency.can_pay,
                type=currency.type
            ).save()
            print('New Currency Added.')
        else:
            prev_cur.name = currency.name
            prev_cur.short_code = currency.short_code
            prev_cur.symbol = currency.symbol
            prev_cur.exchange_rate = currency.exchange_rate
            prev_cur.default = currency.default
            prev_cur.can_withdraw = currency.can_withdraw
            prev_cur.can_pay = currency.can_pay
            prev_cur.type = currency.type
            prev_cur.save()
            print('Currency Updated Successfully.')


def install_demo_user():
    if os.environ.get('FLASK_ENV') == 'development':
        admin_count = Admin.objects.count()
        client_count = Client.objects.count()
        faker = Faker()

        if client_count < 35:
            for _ in range(35 - client_count):
                Client(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email=faker.email(),
                    username=f'user-{_}',
                    password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
                ).save()
            print(f'Clients Created => {35 - client_count}')

        if admin_count < 15:
            for _ in range(15 - admin_count):
                Admin(
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email=faker.email(),
                    username=f'admin-{_}',
                    password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
                ).save()
            print(f'Admin Created => {10 - admin_count}')

    if not Client.get_by_username('user'):
        Client(
            first_name='Jhon',
            last_name='User',
            email='user@something.com',
            username='user',
            password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
        ).save()
        print('Client Created')
    else:
        print('Client Already Created')

    if not Admin.get_by_username('admin'):
        Admin(
            first_name='Jhon',
            last_name='Admin',
            email='admin@something.com',
            username='admin',
            password=bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt())
        ).save()
        print('Admin Created')
    else:
        print('Admin Already Created')
