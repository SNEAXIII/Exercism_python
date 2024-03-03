from datetime import datetime
from operator import attrgetter


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

    def get_format_change_us(self,locale, currency: str) -> str:
        money = f"{abs(self.change / 100):,.2f}"
        if self.change >= 0:
            str_change = f"{currency}{money} "
        else:
            str_change = f"({currency}{money})"
        return f"{str_change:>13}"


def multi_sort(entries: list[LedgerEntry]) -> list[LedgerEntry]:
    return sorted(entries, key=attrgetter("date", "change", "description"))


def create_entry(date, description, change):
    entry = LedgerEntry()
    entry.date = datetime.strptime(date, "%Y-%m-%d")
    entry.description = description
    entry.change = change
    return entry


translate_currency = {
    "USD": "$",
    "EUR": "€"
}
translate_languages = {
    "en_US": ("Date", "Description", "Change", "%m/%d/%Y"),
    "nl_NL": ("Datum", "Omschrijving", "Verandering", "%Y/%m/%d")
}


def format_entries(currency, locale, entries):
    print()
    entries = multi_sort(entries)
    date, description, change, time_format = translate_languages[locale]
    table = f"{date:<10} | {description:<25} | {change:<13}"
    if locale == "en_US":
        currency = translate_currency[currency]

        for entry in entries:
            table += "\n"

            date_str = entry.get_format_time(time_format)
            table += date_str
            table += " | "

            description = f"{entry:str_concat_description}"
            table += description
            table += " | "

            str_change = entry.get_format_change_us(locale,currency)
            table += str_change
        print("\n" + table)
        return table
    elif locale == "nl_NL":

        while len(entries) > 0:
            table += "\n"

            min_entry_index = -1
            for i in range(len(entries)):
                entry = entries[i]
                if min_entry_index < 0:
                    min_entry_index = i
                    continue
                min_entry = entries[min_entry_index]
                if entry.date < min_entry.date:
                    min_entry_index = i
                    continue
                if (
                        entry.date == min_entry.date and
                        entry.change < min_entry.change
                ):
                    min_entry_index = i
                    continue
                if (
                        entry.date == min_entry.date and
                        entry.change == min_entry.change and
                        entry.description < min_entry.description
                ):
                    min_entry_index = i
                    continue
            entry = entries[min_entry_index]
            entries.pop(min_entry_index)

            day = entry.date.day
            day = str(day)
            if len(day) < 2:
                day = "0" + day
            date_str = day
            date_str += "-"
            month = entry.date.month
            month = str(month)
            if len(month) < 2:
                month = "0" + month
            date_str += month
            date_str += "-"
            year = entry.date.year
            year = str(year)
            while len(year) < 4:
                year = "0" + year
            date_str += year
            table += date_str
            table += " | "

            if len(entry.description) > 25:
                for i in range(22):
                    table += entry.description[i]
                table += "..."
            else:
                for i in range(25):
                    if len(entry.description) > i:
                        table += entry.description[i]
                    else:
                        table += " "
            table += " | "

            if currency == "USD":
                change_str = "$ "
                if entry.change < 0:
                    change_str += "-"
                change_dollar = abs(int(entry.change / 100.0))
                dollar_parts = []
                while change_dollar > 0:
                    dollar_parts.insert(0, str(change_dollar % 1000))
                    change_dollar = change_dollar // 1000
                if len(dollar_parts) == 0:
                    change_str += "0"
                else:
                    while True:
                        change_str += dollar_parts[0]
                        dollar_parts.pop(0)
                        if len(dollar_parts) == 0:
                            break
                        change_str += "."
                change_str += ","
                change_cents = abs(entry.change) % 100
                change_cents = str(change_cents)
                if len(change_cents) < 2:
                    change_cents = "0" + change_cents
                change_str += change_cents
                change_str += " "
                while len(change_str) < 13:
                    change_str = " " + change_str
                table += change_str
            elif currency == "EUR":
                change_str = u"€ "
                if entry.change < 0:
                    change_str += "-"
                change_euro = abs(int(entry.change / 100.0))
                euro_parts = []
                while change_euro > 0:
                    euro_parts.insert(0, str(change_euro % 1000))
                    change_euro = change_euro // 1000
                if len(euro_parts) == 0:
                    change_str += "0"
                else:
                    while True:
                        change_str += euro_parts[0]
                        euro_parts.pop(0)
                        if len(euro_parts) == 0:
                            break
                        change_str += "."
                change_str += ","
                change_cents = abs(entry.change) % 100
                change_cents = str(change_cents)
                if len(change_cents) < 2:
                    change_cents = "0" + change_cents
                change_str += change_cents
                change_str += " "
                while len(change_str) < 13:
                    change_str = " " + change_str
                table += change_str
        print("\n" + table)
        return table


currency = "USD"
locale = "en_US"
entries = [
    create_entry("2015-03-12", "Buy aaa", -12345),
    create_entry("2015-03-12", "Buy aaaaaa", -12345),
    create_entry("2028-03-12", "Buy aaaa", 90000),
    create_entry("2015-03-12", "Buy aaaaaaaaa", -12345),
    create_entry("2015-03-12", "Buy aaa", 1000),
    create_entry("2028-03-12", "Buy aaaaaaaaaa", -12345),
    create_entry("2028-03-12", "Buy aaaaaaa", -12345),
    create_entry("2028-03-12", "Buy aaaaaaaaaaaaa", 500),
]
format_entries(currency, locale, entries)
