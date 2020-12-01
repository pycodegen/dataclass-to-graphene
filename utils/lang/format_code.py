from black import format_file_contents, Mode

mode = Mode(
    line_length=5,
)


def format_code(code_str: str) -> str:
    return format_file_contents(code_str, fast=False, mode=mode)
