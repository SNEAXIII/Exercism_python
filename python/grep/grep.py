# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

def checkAndAddLine(is_full_match, pattern, line):
    if is_full_match and pattern + "\n" == line:
        return True
    elif not is_full_match and pattern in line:
        return True
    return False


def grep(pattern, flags, files):
    is_multiple_files: bool = 1 < len(files)
    is_reverse_condition: bool = "-v" in flags
    is_case_sensitive: bool = "-i" not in flags
    is_full_match: bool = "-x" in flags
    is_add_number: bool = "-n" in flags
    # TODO rename this var
    is_l:bool = "-l" in flags

    to_return = ""
    for file_name in files:
        with open(file_name) as file:
            file_content = file.readlines()
        for index, line in enumerate(file_content):
            prefix = ""
            copy_line = line
            if not is_case_sensitive:
                line, pattern = line.lower(), pattern.lower()
            is_grep: bool = checkAndAddLine(is_full_match, pattern, line)
            if is_reverse_condition:
                is_grep = not is_grep
            if not is_grep:
                continue
            if is_l:
                if file_name not in to_return:
                    to_return += f"{file_name}\n"
                continue
            if is_multiple_files:
                prefix += f"{file_name}:"
            if is_add_number:
                prefix += f"{index + 1}:"
            to_return += prefix + copy_line
    return to_return
