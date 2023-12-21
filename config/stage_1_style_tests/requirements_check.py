"""
Checks dependencies
"""
import re
import sys
from pathlib import Path

from config.constants import PROJECT_ROOT


def get_paths() -> list[Path]:
    """
    Returns list of paths to non-python files
    """
    list_with_paths = []
    for file in PROJECT_ROOT.iterdir():
        if file.name in [
            # 'requirements.txt',
            'requirements_qa.txt'
        ]:
            list_with_paths.append(file)
    return list_with_paths


def get_requirements(path: Path) -> list:
    """
    Returns a list of dependencies
    """
    with path.open(encoding='utf-8') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]


def compile_pattern() -> re.Pattern:
    """
    Returns the compiled pattern
    """
    return re.compile(r'\w+(-\w+|\[\w+\])*==\d+(\.\d+)+')


def check_dependencies(lines: list, compiled_pattern: re.Pattern) -> bool:
    """
    Checks that dependencies confirm to the template
    """
    expected = list(sorted(map(str.lower, lines)))
    if expected != list(map(str.lower, lines)):
        print('Dependencies in requirements.txt do not follow sorting rule.')
        print('Expected:')
        print('\n'.join(expected))
        return False
    for line in lines:
        if not re.search(compiled_pattern, line):
            print('Specific dependency in requirements.txt do not conform to the template.')
            print(line)
            return False
    return True


def main() -> None:
    """
    Calls functions
    """
    paths = get_paths()
    compiled_pattern = compile_pattern()
    for path in paths:
        lines = get_requirements(path)
        if not check_dependencies(lines, compiled_pattern):
            sys.exit(1)
        else:
            print(f'{path.name} : OK.')


if __name__ == '__main__':
    main()
