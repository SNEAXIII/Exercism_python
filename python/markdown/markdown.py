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

def tranform_li(line:str):
    is_start_with_star = line.startswith(r"* ")
    if is_start_with_star:
        line = f"<li>{line[2:]}</li>"
    return line,is_start_with_star


def transform_paragraph(line: str):
    if re.match('<h|<ul|<p|<li', line):
        return line
    return f"<p>{line}</p>"


def parse(markdown: str):
    lines = markdown.split('\n')
    in_list = False
    in_list_append = False
    for index, line in enumerate(lines):
        line = transform_header(line)
        line = tranform_strong_em(line)
        if line.startswith(r"* "):
            line = f"<li>{line[2:]}</li>"
            if not in_list:
                in_list = True
                line = '<ul>' + line
        else:
            if in_list:
                in_list_append = True
                in_list = False
        line = transform_paragraph(line)
        if in_list_append:
            line = '</ul>' + line
            in_list_append = False
        lines[index] = line
    if in_list:
        lines[index] += '</ul>'
    return "".join(lines)
