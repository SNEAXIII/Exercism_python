# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

class Grep:
    def __init__(self, pattern, flags, files):
        self.pattern = pattern
        self.files = files
        self.set_flags(flags)
        self.set_sensitivity()
        self.match = self.get_comparaison_method()
        self.add_to_return = self.get_return_method()

    def set_flags(self, flags):
        self.is_multiple_files: bool = 1 < len(self.files)
        self.is_reverse_condition: bool = "-v" in flags
        self.is_case_insensitive: bool = "-i" in flags
        self.is_full_match: bool = "-x" in flags
        self.is_add_number: bool = "-n" in flags
        self.is_return_file_names: bool = "-l" in flags

    def set_sensitivity(self):
        if self.is_case_insensitive:
            self.pattern = self.pattern.lower()

    def get_comparaison_method(self):
        if self.is_full_match:
            return self.is_pattern_equal_line
        return self.is_pattern_is_in_line

    def is_pattern_equal_line(self) -> bool:
        return self.pattern + "\n" == self.current_copy_line

    def is_pattern_is_in_line(self) -> bool:
        return self.pattern in self.current_copy_line

    def get_return_method(self):
        if self.is_return_file_names:
            return self.add_to_return_file_name
        return self.add_to_return_line

    def add_to_return_file_name(self):
        if self.current_file_name not in self.to_return:
            self.to_return += f"{self.current_file_name}\n"

    def add_to_return_line(self):
        prefix = ""
        if self.is_multiple_files:
            prefix += f"{self.current_file_name}:"
        if self.is_add_number:
            prefix += f"{self.current_index + 1}:"
        self.to_return += prefix + self.current_line

    @staticmethod
    def get_file_content(file_name):
        with open(file_name) as file:
            return file.readlines()

    def execute(self):
        self.to_return = ""
        self.current_index = None
        self.current_file_name = None
        self.current_line = None
        self.current_copy_line = None
        for file_name in self.files:
            self.current_file_name = file_name
            file_content = self.get_file_content(file_name)
            for index, line in enumerate(file_content):
                self.current_index = index
                self.current_line = self.current_copy_line = line
                if self.is_case_insensitive:
                    self.current_copy_line = line.lower()
                if self.match() ^ self.is_reverse_condition:
                    self.add_to_return()

    def get_result(self):
        return self.to_return


def grep(str_pattern, str_flags, list_files):
    obj_grep = Grep(str_pattern, str_flags, list_files)
    obj_grep.execute()
    return obj_grep.get_result()
