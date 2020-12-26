# Import documents
from app.documents.setting_document import Setting
from app.documents.currency_document import Currency

# Import Helpers
from app.helpers.dict import AttrDict

# Import Mongoengine Things
from mongoengine import Q

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

    for level in range(1, int(total_generation.value)+1):
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
        prev_cur = Currency.get_by_short_code(currency.short_code).first()
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
            prev_cur.update(
                name=currency.name,
                short_code=currency.short_code,
                symbol=currency.symbol,
                exchange_rate=currency.exchange_rate,
                default=currency.default,
                can_withdraw=currency.can_withdraw,
                can_pay=currency.can_pay,
                type=currency.type
            )
            print('Currency Updated Successfully.')
