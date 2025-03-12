from datetime import date, timedelta
from math import ceil, floor
import calendar


class Period:
    """
    Класс для представления периода работы сотрудника.
    """

    def __init__(self, start: date, end: date, privilege: int | float = 0):
        """
        Инициализация периода работы.

        :param start: Дата начала периода.
        :param end: Дата окончания периода.
        :param privilege: Коэффициент льготы (по умолчанию 0).
        """
        if start > end:
            raise ValueError("Start date must be before end date")  # Проверка корректности дат
        self.start: date = start  # Дата начала периода
        self.end: date = end + timedelta(days=1)  # Дата окончания периода (включительно)
        self.privilege = privilege  # Коэффициент льготы
        self.year = 0  # Количество лет в периоде
        self.month = 0  # Количество месяцев в периоде
        self.day = 0  # Количество дней в периоде
        self.calculate_period()  # Вычисление длительности периода

    def calculate_period(self):
        """
        Вычисляет длительность периода в годах, месяцах и днях с учётом льготного коэффициента.
        """
        # Вычисление дней
        if self.end.day < self.start.day:
            # Если день окончания меньше дня начала, корректируем дни
            days = self.end.day + self.days_in_month(self.start.year, self.start.month)
            self.day = days - self.start.day
            months = self.end.month - self.start.month - 1
        else:
            self.day = self.end.day - self.start.day
            months = self.end.month - self.start.month

        # Вычисление лет и месяцев
        years = self.end.year - self.start.year
        months = years * 12 + months
        self.year = months // 12  # Полные годы
        self.month = months % 12  # Оставшиеся месяцы

        # Учёт льготного коэффициента
        if self.privilege:
            years = floor(self.year * self.privilege)  # Округление лет в меньшую сторону
            remainder_months = round(self.year * self.privilege % 1 * 12)  # Остаток месяцев
            months = floor(self.month * self.privilege) + remainder_months  # Округление месяцев
            remainder_days = self.month * self.privilege % 1 * 30  # Остаток дней
            self.day = self.day * self.privilege  # Учёт льготы для дней
            self.day = ceil(remainder_days + self.day)  # Округление дней в большую сторону
            self.month = months + self.day // 30  # Преобразование дней в месяцы
            self.day %= 30  # Оставшиеся дни
            self.year = years + self.month // 12  # Преобразование месяцев в годы
            self.month %= 12  # Оставшиеся месяцы

    def __str__(self):
        """
        Возвращает строковое представление периода.
        """
        return f"""
        Период с {self.start} до {self.end - timedelta(days=1)}:
            лет - {self.year}  
            месяцев - {self.month}  
            дней - {self.day}
        """

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Возвращает количество дней в указанном месяце и году.

        :param year: Год.
        :param month: Месяц.
        :return: Количество дней в месяце.
        """
        # Использование calendar для получения количества дней в месяце
        return calendar.monthrange(year, month)[1] 


class Employee:
    """
    Класс для представления сотрудника и расчёта его общего стажа.
    """

    def __init__(self, fio: str, periods: list[Period]):
        """
        Инициализация сотрудника.

        :param fio: ФИО сотрудника.
        :param periods: Список периодов работы.
        """
        self.fio = fio  # ФИО сотрудника
        self.periods = periods  # Список периодов работы
        self.year = 0  # Общее количество лет стажа
        self.month = 0  # Общее количество месяцев стажа
        self.day = 0  # Общее количество дней стажа

    def calculate_total_expirience(self) -> Period:
        """
        Вычисляет общий стаж сотрудника на основе всех периодов работы.
        """
        for period in self.periods:
            self.year += period.year  # Суммируем годы
            self.month += period.month  # Суммируем месяцы
            self.day += period.day  # Суммируем дни

        # Преобразование дней в месяцы и месяцев в годы
        self.month += self.day // 30
        self.day %= 30
        self.year += self.month // 12
        self.month %= 12

    def add_period(self, period: Period):
        """
        Добавляет новый период работы сотрудника.

        :param period: Период работы.
        """
        self.periods.append(period)

    def __str__(self):
        """
        Возвращает строковое представление стажа сотрудника.
        """
        return f"""
         Стаж сотрудника {self.fio}:
            лет - {self.year}  
            месяцев - {self.month}  
            дней - {self.day}
        """
    