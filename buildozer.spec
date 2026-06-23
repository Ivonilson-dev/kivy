[app]

# (str) Title of your application
title = Jogo da Memoria

# (str) Package name
package.name = jogodamemoria

# (str) Package domain (needed for android packaging)
package.domain = org.projetos

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,db

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = venv, bin, .buildozer

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow

# (str) Supported orientations (one of landscape, portrait or all)
orientation = portrait

# (str) Presplash image (background color during load)
# android.presplash_color = #1e1e2e

# (bool) Use fullscreen or not
fullscreen = 0

# (list) Permissions
# android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
# android.ndk = 25b

# (bool) Use private storage or shared storage
android.private_storage = 1

p4a.bootstrap = sdl2

# (bool) If True, then automatically accept SDK license agreements.
# This is intended for automation only.
android.accept_sdk_license = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
