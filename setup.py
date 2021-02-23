from setuptools import setup

setup(
    name="encryption",
    options = {
        'build_apps': {
            'include_patterns': [
                '**/*.ef',
            ],
            'gui_apps': {
                'encryption': 'main.py',
            },
            'platforms': [
                'win_amd64'
            ],
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)
