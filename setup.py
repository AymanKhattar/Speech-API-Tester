from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('main.py', base=base, targetName = 'speechApiTester')
]

setup(name='Speech API Tester',
      version = '1.0',
      description = 'Test STT recognition rate over music name dataset',
      options = dict(build_exe = buildOptions),
      executables = executables)
