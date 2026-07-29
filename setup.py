from cx_Freeze import setup, Executable

build_options = {
    'packages': ['numpy', 'sqlite3', 'os', 'sys', 'iso3166', 'tkinter', 'pathlib', 'requests','logging','time','concurrent','matplotlib','json'],
    'excludes': [],
    'include_files': [],
}

# platform
pf = 'Win32GUI' if sys.platform == 'win32' else None

executables = [Executable('mainframe.py', base = pf)]

setup(
    name = 'GTCityStatTracker',
    version = 'v1.0',
    description = "Small program that tracks Round Results in Geotastic's City Streak Highscore Hunter gamemode",
    options = {'build_exe': build_options},
    executables = executables
)