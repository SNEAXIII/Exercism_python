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
    if efficiency >= 60:
        return "orange"
    if efficiency >= 30:
        return "red"
    return "black"


def fail_safe(temperature, neutrons_produced_per_second, threshold):
    product = neutrons_produced_per_second * temperature
    if product <= threshold * .9:
        return "LOW"
    if product <= threshold * 1.1:
        return "NORMAL"
    return "DANGER"
