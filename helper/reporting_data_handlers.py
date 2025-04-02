from datetime import datetime


def reporting_data_handler_db(reporting_data_db: dict):
    """Обработчик массива данных отчета план-факт из БД, только плановые значения
        Args:
            reporting_data_db: массив данных из БД
        Returns:
                Массив данных в едином формате с reporting_data_handler_api
    """
    metric_values_fragment = reporting_data_db['products'][0]['channels'][0]['placements'][0]['dayStats']
    keys_general = ['plan', 'fact', 'tracker', 'percent', 'diff']
    keys_exception = ['plan', 'fact', 'tracker', 'diff']
    processed_data_db = {}
    for date, metrics in metric_values_fragment.items():
        processed_data_db[date] = {}
        for metric in metrics:
            if metric['code'] in ['CONV', 'CR']: # В отчете данные метрики имеют по 4 значения
                metric_values = [metric.get(key, 0) for key in keys_exception if key in metric]
            else:
                metric_values = [metric.get(key, 0) for key in keys_general if key in metric]
            processed_data_db[date][metric['code']] = metric_values
    result_dict = {k: v for k, v in sorted(processed_data_db.items(),
                                           key=lambda item: datetime.strptime(item[0], "%d.%m.%Y") if isinstance(
                                               item[0], str) else item[0])}
    return result_dict


def reporting_data_handler_api(reporting_data_api: dict):
    """Обработчик массива данных отчета план-факт из API, только плановые значения
            Args:
                reporting_data_api: массив данных из API
            Returns:
                Массив данных в едином формате с reporting_data_handler_db
        """
    metric_values_fragment = \
        reporting_data_api['data']['digitalReport']['report']['data'][0]['children'][0]['children'][0]['children']
    keys = ['BUDGET', 'BOUNCES', 'VIMPR', 'CONV', 'CR']
    slices = [slice(0, 5), slice(5, 10), slice(10, 15), slice(15, 19), slice(19, 24)]
    result_dict = {}
    for data in metric_values_fragment:
        date = data['dimensions'][0]['label']
        metrics = [float(i) if '.' in i else int(i) for i in data['metrics']]
        result_dict[date] = {key: metrics[s] for key, s in zip(keys, slices)}
    result_dict = {k: v for k, v in sorted(result_dict.items(),
                                           key=lambda item: datetime.strptime(item[0], "%d.%m.%Y") if isinstance(
                                               item[0], str) else item[0])}
    return result_dict

