from datetime import datetime
from operator import attrgetter

EUR = "EUR"
USD = "USD"
NLNL = "nl_NL"
ENUS = "en_US"
BASE_DATE_FORMAT = "%Y-%m-%d"


class LedgerEntry:
    def __init__(self):
        self.date = None
        self.description = None
        self.change = None

    def get_format_description(self) -> str:
        if len(self.description) > 25:
            return f"{self.description:.22}..."
        return f"{self.description:25}"

    def get_format_time(self, time_format: str) -> str:
        return self.date.strftime(time_format)

    def get_format_change(self, locale: str, currency: str) -> str:
        if locale == ENUS:
            money = f"{abs(self.change) / 100:,.2f}"
            if self.change >= 0:
                str_change = f"{currency}{money} "
            else:
                str_change = f"({currency}{money})"
        elif locale == NLNL:
            money = f"{self.change / 100:,.2f}"
            money = money.replace(",", "_").replace(".", ",").replace("_", ".")
            str_change = f"{currency} {money} "
        else:
            raise Exception(f"Variable {locale = } is not defined")
        return str_change


def create_entry(date: str, description: str, change: int) -> LedgerEntry:
    entry = LedgerEntry()
    entry.date = datetime.strptime(date, BASE_DATE_FORMAT)
    entry.description = description
    entry.change = change
    return entry


def multi_sort(entries: list[LedgerEntry]) -> list[LedgerEntry]:
    return sorted(entries, key=attrgetter("date", "change", "description"))


TRANSLATE_CURRENCY = {
    USD: "$",
    EUR: "€"
}

TRANSLATE_LANGUAGES = {
    ENUS: ("Date", "Description", "Change", "%m/%d/%Y"),
    NLNL: ("Datum", "Omschrijving", "Verandering", "%d-%m-%Y")
}


def format_entries(currency: str, locale: str, entries: list) -> str:
    # Variable setup
    entries = multi_sort(entries)
    currency = TRANSLATE_CURRENCY[currency]
    date, description, change, time_format = TRANSLATE_LANGUAGES[locale]
    table = f"{date:<10} | {description:<25} | {change:<13}"

    # Looping into each sorted entry
    for entry in entries:
        date_str = entry.get_format_time(time_format)
        description = entry.get_format_description()
        str_change = entry.get_format_change(locale, currency)
        table += f"\n{date_str} | {description} | {str_change:>13}"

    return table
