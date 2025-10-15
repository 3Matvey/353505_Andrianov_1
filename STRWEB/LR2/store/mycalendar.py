from datetime import datetime, timedelta, timezone


def get_calendar(self, year, month):
        months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]

        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        first_day = datetime(year, month, 1)

        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
            next_month = 1
            next_year = year + 1
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            next_month = month + 1
            next_year = year

        if month == 1:
            prev_month = 12
            prev_year = year - 1
        else:
            prev_month = month - 1
            prev_year = year

        num_days = last_day.day

        current_date = timezone.localtime().date()

        first_weekday = first_day.weekday()

        calendar_rows = []

        month_title = f"{months[month-1]} {year}"

        weekdays_row = weekdays

        current_day = 1
        current_row = ['  ' for _ in range(first_weekday)]

        while current_day <= num_days:
            while len(current_row) < 7 and current_day <= num_days:
                is_current = (current_day == current_date.day and
                            month == current_date.month and
                            year == current_date.year)

                day_str = f"{current_day:2d}"
                current_row.append({
                    'day': day_str,
                    'is_current': is_current
                })
                current_day += 1

            while len(current_row) < 7:
                current_row.append('  ')

            calendar_rows.append(current_row)
            current_row = []

        return {
            'title': month_title,
            'weekdays': weekdays_row,
            'rows': calendar_rows,
            'prev_month': prev_month,
            'prev_year': prev_year,
            'next_month': next_month,
            'next_year': next_year,
            'current_month': month,
            'current_year': year
        }
