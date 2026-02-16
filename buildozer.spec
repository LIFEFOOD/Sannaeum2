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
source.include_exts = py,png,jpg,kv,txt,json

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Application versioning
version = 1.0.0
version.code = 1

# (list) Application requirements - pyjnius 유지 (클립보드용)
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
android.archs = armeabi-v7a, arm64-v8a

# (bool) Enable AndroidX support
android.use_androidx = True

# ★ 중요: Gradle dependencies (작은따옴표 제거)
android.gradle_dependencies = androidx.core:core:1.9.0

# Gradle 데몬 메모리 설정
android.gradle_options = -Xmx2048M

# (str) Package format (aab for Play Store)
android.package_format = aab

# ===== 키스토어 설정 (릴리스 빌드용) =====
# (str) Full path to the keystore
android.keystore = %(source.dir)s/sannaeeum.keystore

# ★ 중요: 환경변수 형식 변경 (중괄호 제거)
android.keystore_password = $KEYSTORE_PASSWORD

# (str) Keystore alias - 직접 입력 (고정)
android.keyalias = sannaeeum

# ★ 중요: 환경변수 형식 변경 (중괄호 제거)
android.keyalias_password = $KEY_PASSWORD

# (bool) Release build
android.release_mode = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.2.9519653

# (bool) Ignore environment NDK variables
android.ignore_environment_ndk = True

# (str) Java version
android.java_version = 11

# (str) The p4a bootstrap to use
android.bootstrap = sdl2

# (bool) Compile the python in the pyc format
android.pyc = True

# (bool) Copy the packaged asset by
android.copy_libs = True

# (bool) Clean build
android.clean_on_restart = False

# (bool) Use the new toolchain
android.new_toolchain = True

# (bool) Enable logging
android.log_打包信息 = True

# ★ 중요: APK 분할 설정 (용량 최적화)
android.split_per_abi = True

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme
android.apptheme = @android:style/Theme.NoTitleBar

# (bool) Add gradle dependencies offline
android.gradle_offline = False

# (bool) Enable debug symbols
android.debug_symbols = False

#
# Logging
#

# (str) Log level (debug, info, warning, error)
log_level = 2

# (bool) Show the commands executed by buildozer
debug_commands = False

# (bool) Show the debug output of the build
debug_build = False

# (bool) Log to file
log_to_file = True

# (str) Log file name
log_filename = buildozer.log

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if the application is built as root
warn_on_root = 1

# (str) Path to the build directory
build_dir = ./.buildozer

# (str) Path to the bin directory
bin_dir = ./bin

# (int) Maximum number of concurrent threads for build
jobs = 4