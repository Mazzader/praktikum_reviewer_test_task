import datetime as dt # Нет смысла импортировать весь модуль, можно испортировать лишь конкретную часть, которую вы используете(datetime)


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount # Думаю стоит подумать насчет инкапсуляции и сделать get и set методы для amount и date
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date()) # если вы используете конструкцию if not лучше конкретно указать default value = None для date.
            # if not лучше использовать в одной строке, чтобы повысить читаемость кода, хотя я бы вообще отказался от однострочника здесь.
        self.comment = comment


class Calculator:
    def __init__(self, limit): # лучше сделать records опциональным аргументом и передавать туда пустой писок по умолчанию,
                               #либо назвать переменную _record, если доступ извне не предполагается совсем
        self.limit = limit 
        self.records = []

    def add_record(self, record): # стоит указать тип record, который мы ожидаем и делать проверку, соответствует ли запись типу, который мы ждем
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records: # имя переменной должно быть с маленькой буквы, в данном случае вообще получилось что мы обращаемся к классу Record
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        # (today - record.date).days лучше вынести в отдельную переменную.
        # скобки у if стоит убрать. Вообще строчки 36-41 можно првратить в однострочник
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал' # Нужно пользоваться .format вместо f'' строк.
        else:
            return('Хватит есть!')
        # строки 48-52 можно превратить в однострочник, строку из if statement лучше вынести в отдельную переменную 
        # и отформатировать заранее, сделать проверку и вернуть переменную, содержащую строку.


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # Если мы принимаем это от пользователя, лучше сделать конвертацию внутри функции и убрать константы из класса, если получение от пользователя не 
        # предусмотрено, стоит убрать это из функции и обращаться через self. Судя по названию переменных здесь подразумеваются константы, в таком случае
        # не стоит передавать их как параметры функции и уж точно не стоит давать возможность их измпенять так или иначе.
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # метод из-за такого колличества if получился очень большим. Во первых лучше посмотреть в сторону switch case, который добавили в python 3.10,
        # во вторых нужно обязательно вынести сами проверки в отдельные фнкции! Потому что в названии этого метода однозначно указывается, что мы лишь 
        # получаем остаток на сегодняшний день и нет ни слова про проверку, а еще если нам потребуется изменить проверку  - удобнее будет редактировать отдельную
        # функцию, отвечающую за проверку, не трогая при этом функцию получения остатка.
        if currency == 'usd': # currency_type?)
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}' # убрать f строки
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
