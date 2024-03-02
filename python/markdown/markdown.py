from re import search, match


def transform_header_to_html(line: str):
    find = search("^#{1,6}\s", line)
    if not find:
        return line
    count = len(find.group())
    return f"<h{count - 1}>{line[count:]}</h{count - 1}>"


def transform_font_weight_to_html(line: str):
    dict_to_replace = {
        "__": ("<strong>", "</strong>"),
        "_": ("<em>", "</em>")
    }
    for symbol, tuple_substitute in dict_to_replace.items():
        count = line.count(symbol)
        line = line.replace(symbol, "%s", count // 2 * 2)
        line %= tuple_substitute * (count // 2)
    return line


def transform_list_element_to_html(line: str, list_map_in_list: list):
    is_in_list = line.startswith(r"* ")
    list_map_in_list.append(is_in_list)
    if is_in_list:
        line = f"<li>{line[2:]}</li>"
    return line


def transform_paragraph_to_html(line: str):
    if match('<h|<p|<li', line):
        return line
    return f"<p>{line}</p>"


def add_ul_tags(lines: list, list_map_in_list: list):
    if not any(list_map_in_list):
        return
    open_ul, close_ul = "<ul>", "</ul>"
    is_previously_in_list = False
    for index, is_currently_in_list in enumerate(list_map_in_list):
        if is_currently_in_list and not is_previously_in_list:
            lines[index] = open_ul + lines[index]
        if not is_currently_in_list and is_previously_in_list:
            lines[index - 1] += close_ul
        is_previously_in_list = is_currently_in_list
    if is_previously_in_list:
        lines[-1] += close_ul


def process_line(line: str, list_map_in_list: list):
    line = transform_header_to_html(line)
    line = transform_font_weight_to_html(line)
    line = transform_list_element_to_html(line, list_map_in_list)
    line = transform_paragraph_to_html(line)
    return line


def parse(markdown: str):
    lines = markdown.split('\n')
    list_map_in_list = []
    for index, line in enumerate(lines):
        line = process_line(line, list_map_in_list)
        lines[index] = line
    add_ul_tags(lines, list_map_in_list)
    return "".join(lines)
