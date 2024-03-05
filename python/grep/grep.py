

def grep(pattern, flags, files):
    is_reverse_condition = "-v" in flags
    is_case_sensitive = "-i" not in flags
    is_full_match = "-x" in flags
    is_add_number = "-n" in flags
    to_return = ""
    for file in files:
        with open(file, encoding="utf-8") as content:

            for index, line in enumerate(content.readlines()):
                copy_line = line
                if not is_case_sensitive:
                    line, pattern = line.lower(), pattern.lower()
                if is_full_match:
                    if pattern + "\n" != line:
                        copy_line = ""
                else:
                    if pattern not in line:
                        copy_line = ""
                if is_add_number and copy_line:
                    copy_line = f"{index+1}:{copy_line}"
                to_return += copy_line
    return to_return
