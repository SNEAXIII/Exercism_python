from datetime import datetime
from operator import attrgetter

EUR = "EUR"
USD = "USD"
NLNL = "nl_NL"
ENUS = "en_US"


class LedgerEntry:
    def __init__(self):
        self.date = None
        self.description = None
        self.change = None

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "str_concat_description":
                if len(self.description) > 25:
                    return f"{self.description:.22}..."
                return f"{self.description:25}"

    def get_format_time(self, time_format: str) -> str:
        return self.date.strftime(time_format)

    def get_format_change(self, locale, currency: str) -> str:
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
        return str_change


def multi_sort(entries: list[LedgerEntry]) -> list[LedgerEntry]:
    return sorted(entries, key=attrgetter("date", "change", "description"))


def create_entry(date, description, change):
    entry = LedgerEntry()
    entry.date = datetime.strptime(date, "%Y-%m-%d")
    entry.description = description
    entry.change = change
    return entry


translate_currency = {
    USD: "$",
    EUR: "€"
}
translate_languages = {
    ENUS: ("Date", "Description", "Change", "%m/%d/%Y"),
    NLNL: ("Datum", "Omschrijving", "Verandering", "%d-%m-%Y")
}


def format_entries(currency, locale, entries):
    currency = translate_currency[currency]
    entries = multi_sort(entries)
    date, description, change, time_format = translate_languages[locale]
    table = f"{date:<10} | {description:<25} | {change:<13}"

    for entry in entries:
        date_str = entry.get_format_time(time_format)
        description = f"{entry:str_concat_description}"
        str_change = entry.get_format_change(locale, currency)
        table += f"\n{date_str} | {description} | {str_change:>13}"
    return table
