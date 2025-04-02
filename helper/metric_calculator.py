import random


class MetricsCalculator:
    BUDGET: int = random.randint(a=100000, b=2000000)
    IMPS: int = random.randint(a=100000, b=2000000)
    CLICKS: int = random.randint(a=100000, b=2000000)
    CTR: int = ''
    PI = ''
    CRR = ''
    CV = ''
    ROAS = ''
    REACH = ''
    CPT = ''
    VTR = ''
    CPV = ''
    VIEWABILITY = ''

    @staticmethod
    def format_value(value):
        f_value = str(f'{value:,.2f}').replace(',', ' ')
        if f_value[-1] == '0':
            f_value = f_value.rstrip('0')
        if f_value[-1] == '.':
            f_value = f_value.rstrip('.')
        elif f_value[-2:] == '.0':
            f_value = value.rstrip('.0')
        return f_value

    @staticmethod
    def formula_for_cpm() -> str:
        cpm: float = MetricsCalculator.BUDGET * 1000 / MetricsCalculator.IMPS
        return MetricsCalculator.format_value(cpm)

    @staticmethod
    def formula_for_cpc() -> str:
        cpc: float = MetricsCalculator.BUDGET / MetricsCalculator.CLICKS
        return MetricsCalculator.format_value(cpc)

    @staticmethod
    def formula_for_ctr() -> str:
        ctr: float = MetricsCalculator.CLICKS / MetricsCalculator.IMPS * 100
        return MetricsCalculator.format_value(ctr)
