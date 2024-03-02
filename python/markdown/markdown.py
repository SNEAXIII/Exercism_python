import re


def transform_header(line: str):
    find = re.search("^#{1,6}\s", line)
    if not find:
        return line
    count = len(find.group())
    return f"<h{count - 1}>{line[count:]}</h{count - 1}>"


dict_to_replace = {
    "__": ("<strong>", "</strong>"),
    "_": ("<em>", "</em>")
}


def tranform_strong_em(line: str):
    for symbol, tuple_substitute in dict_to_replace.items():
        count = line.count(symbol)
        line = line.replace(symbol, "%s", count // 2 * 2)
        line %= tuple_substitute * (count // 2)
    return line


def parse(markdown: str):
    print()
    number_of_star = markdown.count("*")
    print(f"{number_of_star = }")
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for line in lines:
        line = transform_header(line)
        line = tranform_strong_em(line)
        m = re.match(r'\* (.*)', line)
        if m:
            if not in_list:
                in_list = True
                curr = m.group(1)
                line = '<ul><li>' + curr + '</li>'
            else:
                curr = m.group(1)
                line = '<li>' + curr + '</li>'
        else:
            if in_list:
                in_list_append = True
                in_list = False
        m = re.match('<h|<ul|<p|<li', line)
        if not m:
            line = '<p>' + line + '</p>'
        if in_list_append:
            line = '</ul>' + line
            in_list_append = False
        res += line
    if in_list:
        res += '</ul>'
    return res
