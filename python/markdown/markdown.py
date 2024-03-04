from re import match


def check_and_transform_header_to_html(line: str) -> str:
    if find := match("^#{1,6}\s", line):
        count = len(find.group())
        return f"<h{count - 1}>{line[count:]}</h{count - 1}>"
    return line


def check_and_transform_font_weight_to_html(line: str) -> str:
    tuple_font_weight = (
        ("__", ("<strong>", "</strong>")),
        ("_", ("<em>", "</em>"))
    )

    for symbol, tuple_substitute in tuple_font_weight:
        count = line.count(symbol)
        line = line.replace(symbol, "%s", count // 2 * 2)
        line %= tuple_substitute * (count // 2)
    return line


def check_is_list_element(line: str) -> bool:
    return line.startswith(r"* ")


def transform_list_element_to_html(line: str) -> str:
    return f"<li>{line[2:]}</li>"


def check_is_paragraph(line: str) -> bool:
    return match('<h|<li', line)


def transform_paragraph_to_html(line: str) -> str:
    return f"<p>{line}</p>"


def add_ul_tags(lines: list):
    list_map_in_list = tuple(line.startswith("<li>") for line in lines)
    if not any(list_map_in_list):
        return lines
    # if there is any <li> in lines, we need to add <ul>
    # at the begining and the end of the list
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

    return lines


def process_line(line: str):
    line = check_and_transform_header_to_html(line)
    line = check_and_transform_font_weight_to_html(line)
    if check_is_list_element(line):
        line = transform_list_element_to_html(line)
    if check_is_paragraph(line):
        line = transform_paragraph_to_html(line)
    return line


def parse(markdown: str):
    lines = markdown.split('\n')
    for index, line in enumerate(lines):
        line = process_line(line)
        lines[index] = line
    lines = add_ul_tags(lines)
    return "".join(lines)
