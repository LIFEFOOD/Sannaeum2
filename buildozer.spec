[app]

# (str) Title of your application
title = 산내음 링크

# (str) Package name
package.name = sannaeeumlink

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sannaeeum

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,ttf,txt,json

# (str) Application versioning
version = 1.0.0
version.code = 1

# (list) Application requirements - 중요! android 추가
requirements = python3,kivy==2.1.0,pyjnius,android

# (str) Icon of the application
icon.filename = %(source.dir)s/res/drawable/icon.png

# (str) Supported orientation
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK / AAB will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = armeabi-v7a

# (bool) Enable AndroidX support
android.use_androidx = True

# Gradle dependencies
android.gradle_dependencies = 'androidx.core:core:1.9.0'

# Gradle 데몬 메모리 설정
android.gradle_options = -Xmx2048M

# (str) Package format (apk or aab)
android.package_format = aab

# ===== 키스토어 설정 (릴리스 빌드용) =====
# (str) Full path to the keystore
android.keystore = %(source.dir)s/sannaeeum.keystore

# (str) Keystore password - GitHub Secrets에서 전달
android.keystore_password = ${KEYSTORE_PASSWORD}

# (str) Keystore alias - 직접 입력 (고정)
android.keyalias = sannaeeum

# (str) Key password - GitHub Secrets에서 전달
android.keyalias_password = ${KEY_PASSWORD}

# (bool) Release build
android.release_mode = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.2.9519653

# (str) The p4a bootstrap to use
android.bootstrap = sdl2

# (bool) Compile the python in the pyc format
android.pyc = True

#
# Logging
#

# (str) Log level (debug, info, warning, error)
log_level = 2

# (bool) Show the commands executed by buildozer
debug_commands = True

# (bool) Show the debug output of the build
debug_build = True

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if the application is built as root
warn_on_root = 1
