import pytest
from contextlib import nullcontext as does_not_raise
from src.employee import Period, Employee
from datetime import date


class TestPeriod:
    """
    Класс для тестирования класса Period.
    """

    @pytest.mark.parametrize(
        'start, end, privilege, res, expectation',
        [
            # Тестовые случаи для метода calculate_period
            (date(2006, 8, 16), date(2023, 10, 18), 0, (17, 2, 3), does_not_raise()),  # 7.1
            (date(2009, 1, 15), date(2023, 3, 9), 0, (14, 1, 26), does_not_raise()),  # 7.2
            (date(2013, 4, 16), date(2023, 9, 1), 0, (10, 4, 16), does_not_raise()),  # 7.2
            (date(2019, 5, 15), date(2023, 12, 14), 0, (4, 7, 0), does_not_raise()),  # 7.3
            (date(2014, 10, 18), date(2023, 5, 11), 0, (8, 6, 25), does_not_raise()),  # 7.4
            (date(2016, 7, 1), date(2023, 4, 30), 0, (6, 10, 0), does_not_raise()),  # 8
            (date(2016, 1, 1), date(2023, 12, 31), 0, (8, 0, 0), does_not_raise()),
            (date(2016, 1, 1), date(2023, 2, 28), 0, (7, 2, 0), does_not_raise()),
            (date(2016, 1, 1), date(2024, 2, 29), 0, (8, 2, 0), does_not_raise()),
            (date(2017, 9, 18), date(2023, 5, 10), 0, (5, 7, 23), does_not_raise()),  # 9
            (date(2017, 9, 18), date(2023, 5, 10), 2, (11, 3, 16), does_not_raise()),  # 9
            (date(2017, 9, 18), date(2023, 5, 10), 1.5, (8, 5, 20), does_not_raise()),  # 9
            (date(2017, 9, 18), date(2017, 9, 17), 0, (8, 5, 20), pytest.raises(ValueError)),  # 9
        ]
    )
    def test_calculate_period(self, start, end, privilege, res, expectation):
        """
        Тестирование метода calculate_period класса Period.
        
        :param start: Дата начала периода.
        :param end: Дата окончания периода.
        :param privilege: Коэффициент льготы.
        :param res: Ожидаемый результат (годы, месяцы, дни).
        :param expectation: Ожидаемое поведение (исключение или его отсутствие).
        """
        with expectation:
            period = Period(start, end, privilege)  # Создаем объект Period
            assert (period.year, period.month, period.day) == res  # Проверяем результат


class TestEmployee:
    """
    Класс для тестирования класса Employee.
    """

    @pytest.mark.parametrize(
        'fio, periods, res, expectation',
        [
            # Тестовый случай для метода calculate_total_experience
            (
                "Иванов Иван Иванович",
                [
                    Period(date(2003, 3, 27), date(2014, 1, 12)),
                    Period(date(2014, 1, 13), date(2019, 11, 3)),
                    Period(date(2019, 11, 4), date(2024, 2, 18)),
                ],
                (20, 10, 24),  # Ожидаемый результат (годы, месяцы, дни)
                does_not_raise()
            ),  # 6
        ]
    )
    def test_calculate_total_experience(self, fio, periods, res, expectation):
        """
        Тестирование метода calculate_total_experience класса Employee.
        
        :param fio: ФИО сотрудника.
        :param periods: Список периодов работы.
        :param res: Ожидаемый результат (годы, месяцы, дни).
        :param expectation: Ожидаемое поведение (исключение или его отсутствие).
        """
        with expectation:
            employee = Employee(fio, periods)  # Создаем объект Employee
            employee.calculate_total_expirience()  # Вычисляем общий стаж
            assert (employee.year, employee.month, employee.day) == res  # Проверяем результат
