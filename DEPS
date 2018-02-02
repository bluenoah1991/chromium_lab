deps = {
  'buildtools':
    'https://chromium.googlesource.com/chromium/buildtools.git@437a616be5b2056336ed3ca5c33c41f7788ede09',
  'third_party/depot_tools':
    'https://chromium.googlesource.com/chromium/tools/depot_tools.git@fd4ad2416554c43f6ecd2c9c62ab5914f521c9ad'
}

hooks = [
  # Pull GN binaries. This needs to be before running GYP below.
  {
    'name': 'gn_win',
    'pattern': '.',
    'action': [ 'python',
                'third_party/depot_tools/download_from_google_storage.py',
                '--no_resume',
                '--no_auth',
                '--bucket', 'chromium-gn',
                '-s', 'buildtools/win/gn.exe.sha1',
    ],
  }
]