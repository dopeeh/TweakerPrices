from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]
packages = ["idna", "selenium", "six", 'pkg_resources._vendor']
options = {
    'build_exe': {
        'packages':packages,
        'include_files': ['Input/'],
    },
}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)