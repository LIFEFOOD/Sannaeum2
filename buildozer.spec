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

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Application versioning
version = 1.0.0
version.code = 1

# (list) Application requirements
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
android.gradle_options = -Xmx2048M --stacktrace --info

# (str) Package format (apk or aab)
android.package_format = aab

# ===== 키스토어 설정 (릴리스 빌드용) =====
# (str) Full path to the keystore
android.keystore = %(source.dir)s/sannaeeum.keystore

# (str) Keystore password - GitHub Secrets에서 전달
# 실제 비밀번호: sskk052301**01 (KEYSTORE_PASSWORD에 등록됨)
android.keystore_password = ${KEYSTORE_PASSWORD}

# (str) Keystore alias - 직접 입력 (고정)
android.keyalias = sannaeeum

# (str) Key password - GitHub Secrets에서 전달
# 실제 비밀번호: sskk052301**01 (KEY_PASSWORD에 등록됨)
# ※ 키스토어 비밀번호와 동일한 값 사용
android.keyalias_password = ${KEY_PASSWORD}

# (bool) Release build
android.release_mode = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.2.9519653

# (str) NDK path - 명시적 지정 (충돌 방지)
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

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

# (list) Extra Java source files
android.add_src =

# (list) Extra libraries to include
android.add_libs =

# (list) Extra Android manifest options
android.extra_manifest_xml =

# (bool) Use the new toolchain
android.new_toolchain = True

# (str) Ant path (if needed)
# android.ant_path =

# (str) SDK path (if needed)
# android.sdk_path =

# (str) NDK path (already set above)
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# (bool) Use the older toolchain
# android.old_toolchain = False

# (bool) Enable logging of the android打包信息
android.log_打包信息 = True

#
# iOS specific (필요 없으면 무시)
#
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

#
# Logging
#

# (str) Log level (debug, info, warning, error)
log_level = 2

# (bool) Show the commands executed by buildozer
debug_commands = True

# (bool) Show the debug output of the build
debug_build = True

# (bool) Log to file
log_to_file = True

# (str) Log file name
log_filename = buildozer.log

# (bool) Log the host information
log_host = True

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

# (str) The directory to look for the Android SDK
# android.sdk_path =

# (str) The directory to look for the Android NDK
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# (str) The directory to look for the Android ANT
# android.ant_path =

# (str) The directory to look for the Android SDK Tools
# android.sdk_tools_path =

# (str) The directory to look for the Android NDK standalone toolchain
# android.ndk_toolchain_path =

# (str) The directory to look for the Android NDK toolchain
# android.toolchain_path =
