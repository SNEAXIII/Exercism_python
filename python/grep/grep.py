# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class Grep:
    def __init__(self, pattern, flags, files):
        self.files = files
        self.set_flags(flags, pattern)
    def set_flags(self, flags, pattern):
        self.is_multiple_files = 1 < len(self.files)
        self.is_reverse_condition = "-v" in flags
        self.is_full_match = "-x" in flags
        self.is_add_number = "-n" in flags
        self.is_add_file_names = "-l" in flags
        self.is_case_insensitive = "-i" in flags
        self.pattern = pattern.lower() if self.is_case_insensitive else pattern

    def is_match(self,current_copy_line):
        if self.is_full_match:
            return self.pattern + "\n" == current_copy_line
        return self.pattern in current_copy_line

    def add_to_return(self,current_line,index,current_file_name):
        if self.is_add_file_names:
            if current_file_name not in self.to_return:
                self.to_return += f"{current_file_name}\n"
            return
        prefix = ""
        if self.is_multiple_files:
            prefix += f"{current_file_name}:"
        if self.is_add_number:
            prefix += f"{index + 1}:"
        self.to_return += prefix + current_line

    @staticmethod
    def get_file_content(file_name):
        with open(file_name) as file:
            return file.readlines()

    def get_result(self):
        self.to_return = ""
        for current_file_name in self.files:
            file_content = self.get_file_content(current_file_name)
            for index, line in enumerate(file_content):
                current_line = current_copy_line = line
                if self.is_case_insensitive:
                    current_copy_line = line.lower()
                if self.is_match(current_copy_line) ^ self.is_reverse_condition:
                    self.add_to_return(current_line,index,current_file_name)
        return self.to_return


def grep(str_pattern, str_flags, list_files):
    obj_grep = Grep(str_pattern, str_flags, list_files)
    return obj_grep.get_result()
