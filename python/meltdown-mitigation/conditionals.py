"""Functions to prevent a nuclear meltdown."""


def is_criticality_balanced(temperature, neutrons_emitted):
    is_right_temp = temperature < 800
    is_enough_neutrons = neutrons_emitted > 500
    is_product_less_than_500000 = temperature * neutrons_emitted < 500000
    return all((is_right_temp, is_enough_neutrons, is_product_less_than_500000))


def reactor_efficiency(voltage, current, theoretical_max_power):
    efficiency = ((current * voltage) / theoretical_max_power) * 100
    if 100 >= efficiency >= 80:
        return "green"
    elif efficiency >= 60:
        return "orange"
    elif efficiency >= 30:
        return "red"
    return "black"


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    """Assess and return status code for the reactor.

    :param temperature: int or float - value of the temperature in kelvin.
    :param neutrons_produced_per_second: int or float - neutron flux.
    :param threshold: int or float - threshold for category.
    :return: str - one of ('LOW', 'NORMAL', 'DANGER').

    1. 'LOW' -> `temperature * neutrons per second` < 90% of `threshold`
    2. 'NORMAL' -> `temperature * neutrons per second` +/- 10% of `threshold`
    3. 'DANGER' -> `temperature * neutrons per second` is not in the above-stated ranges
    """
    n = neutrons_produced_per_second*temperature

    print(n,threshold)
    if threshold <= n <= threshold * .9:
        return 'LOW'
    if n <= threshold * .1:
        return 'NORMAL'
    return 'DANGER'
fail_safe(10, 399, 10000)