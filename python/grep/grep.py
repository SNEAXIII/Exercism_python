def check_and_transform_if_match_entiere_line(line: str, pattern: str, is_case_sensitive: bool) -> str:
    copy_line = line
    if not is_case_sensitive:
        line, pattern = line.lower(), pattern.lower()
    if pattern + "\n" == line:
        return copy_line
    return ""


def check_and_transform_if_str_contain_substr(line: str, pattern: str, is_case_sensitive: bool) -> str:
    copy_line = line
    if not is_case_sensitive:
        line, pattern = line.lower(),pattern.lower()
    if pattern in line:
        return copy_line
    return ""


def grep(pattern, flags, files):
    is_reverse_condition = "-v" in flags
    is_case_sensitive = "-i" not in flags
    check_and_transform_if_match_method = check_and_transform_if_match_entiere_line if "-x" in flags else check_and_transform_if_str_contain_substr

    for file in files:
        with open(file, encoding="utf-8") as content:
            to_return = ""
            for index,line in enumerate(content.readlines()):
                to_return += check_and_transform_if_match_method(line,pattern,is_case_sensitive)
    return to_return
