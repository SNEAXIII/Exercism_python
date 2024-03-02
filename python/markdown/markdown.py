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


def transform_li(line: str, list_map_in_list: list):
    is_start_with_star = line.startswith(r"* ")
    list_map_in_list.append(is_start_with_star)
    if is_start_with_star:
        line = f"<li>{line[2:]}</li>"
    return line


def transform_paragraph(line: str):
    if re.match('<h|<p|<li', line):
        return line
    return f"<p>{line}</p>"


def transform_ul(lines: list, list_map_in_list: list):
    open_ul,close_ul = "<ul>", "</ul>"
    is_previously_in_list = False
    for index, is_currently_in_list in enumerate(list_map_in_list):
        if is_currently_in_list and not is_previously_in_list:
            lines[index] = open_ul + lines[index]
        if not is_currently_in_list and is_previously_in_list:
            lines[index - 1] += close_ul
        is_previously_in_list = is_currently_in_list
    if is_previously_in_list:
        lines[index] += close_ul


def parse(markdown: str):
    lines = markdown.split('\n')
    print(f"{lines = }")
    list_map_in_list = []
    for index, line in enumerate(lines):
        line = transform_header(line)
        line = tranform_strong_em(line)
        line = transform_li(line, list_map_in_list)
        line = transform_paragraph(line)
        lines[index] = line
    print(list_map_in_list)
    if any(list_map_in_list):
        transform_ul(lines,list_map_in_list)
    print(f"{lines = }")
    return "".join(lines)


print(parse("# Start a list\n* Item 1\n* Item 2\nEnd a list"))
print("<h1>Start a list</h1><ul><li>Item 1</li><li>Item 2</li></ul><p>End a list</p>")
