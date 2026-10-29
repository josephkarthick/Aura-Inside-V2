def percentage(current, previous):
    if previous == 0:
        return 100 if current > 0 else 0  # handle division by zero
    return round(((current - previous) / previous) * 100, 2)

