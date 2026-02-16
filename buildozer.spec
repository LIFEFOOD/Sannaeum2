[app]

# (str) Title of your application
title = 산내음 링크

# (str) Package name
package.name = sannaeeumlink

# (str) Package domain (needed for android/ios packaging)
package.domain = org.sannaeeum

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let everything but .git)
source.include_exts = py,png,jpg,kv,ttf,txt

# (list) Source files to exclude (e.g. you might don't want to upload your
source.exclude_exts = spec

# (list) List of directory to exclude from the source
#source.exclude_dirs = tests, bin

# (list) List of patterns to ignore
#source.exclude_patterns = license,images/*.jpg

# (str) Application versioning (method 1: manual version)
version = 0.1

# (str) Application versioning (method 2: regex from a file)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pyjnius

# (str) Custom source folders for requirements
#requirements.source.kivy = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/res/drawable/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# OSX Specific
#

#
# author = © Copyright Info

# change the major version of python used by the app
osx.python_version = 3

# Kivy version to use
osx.kivy_version = 2.2.1

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, grey, lightgrey, darkgrey, aqua, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
#android.presplash_color = #FFFFFF

# (str) Presplash animation using Lottie format.
# see https://lottiefiles.com/ for examples and https://airbnb.design/lottie/
# for general documentation.
# Lottie files can be created using various tools like Adobe After Effect or Synfig.
#android.presplash_lottie = "path/to/lottie/file.json"

# (str) Adaptive icon of the application (used if Android API level is 26+ at runtime)
#icon.adaptive_foreground.filename = %(source.dir)s/data/icon_fg.png
#icon.adaptive_background.filename = %(source.dir)s/data/icon_bg.png

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 33  # deprecated, but kept for compatibility

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
#android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.renpy.android.PythonActivity

# (list) Pattern of file to copy (ignore raw file)
# android.copy_libs = libs/main/*.so

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
# 빌드 시간과 안정성을 위해 하나의 아키텍처만 선택 (armeabi-v7a가 가장 호환성 좋음)
android.archs = armeabi-v7a

# (int) Override the default loading dialog if desired
#android.loading_dialog = 0

# (int) Loading dialog corner radius
#android.loading_dialog_radius = 20

# (bool) Loading dialog progress bar
#android.loading_dialog_progress = True

# (str) Screens of the application
#android.screens = small,normal,large,xlarge

# (str) Display orientation (used only with android.entrypoint != org.renpy.android.PythonActivity)
#android.orientation = portrait

# (list) Java classes to add as activities
#android.add_activities = org.example.MyActivity,org.example.SecondActivity

# (list) Java classes to add as services
#android.add_services = org.example.MyService

# (bool) Skip full validation of the manifest
#android.skip_manifest_validation = False

# (str) Validation modes for the manifest: 'basic' or 'full'
#android.manifest_validation_mode = basic

# (bool) Ignore support for older devices with GLES version < 2
#android.gles_ignore = False

# (int) OpenGL ES version to require
#android.gl = 2

# (bool) Indicate that the application should handle it's own GPU death
#android.handle_gpu_death = False

# (bool) Indicate that the application should be debuggable
android.debug = False  # 릴리스 빌드용

# (bool) Enable AndroidX support
android.use_androidx = True

# android.gradle_dependencies = 'androidx.core:core:1.7.0'  ← 주석 처리
android.gradle_dependencies =

# Gradle 데몬 메모리 설정
android.gradle_options = -Xmx1024M

# ===== APK 파일명 설정 (유지) =====
# (str) Filename for the release APK
android.filename = sannaeeum

# (str) Package format (apk or aab)
android.package_format = apk

# ===== 키스토어 설정 (릴리스 빌드용) =====
# (str) Full path to the keystore
android.keystore = %(source.dir)s/sannaeeum.keystore

# (str) Keystore password - GitHub Actions에서는 환경변수로 대체됨
android.keystore_password = $(KEYSTORE_PASSWORD)

# (str) Keystore alias
android.keystore_alias = sannaeeum

# (str) Key password - GitHub Actions에서는 환경변수로 대체됨
android.key_password = $(KEY_PASSWORD)

# (bool) Indicate if it's a release build
android.release = True

# (str) The name of the bundle (aab file)
#android.bundle_name = sannaeeumlink

# (str) Authority used for file provider, you can set your package name with ${PACKAGE_NAME}
#android.authority = ${PACKAGE_NAME}.fileprovider

# (bool) Enable logging of Android打包信息
#android.log_打包信息 = True

# (bool) Copy the packaged asset by
#android.clean_on_restart = True

# (bool) Fix the default distribution if it doesn't match the one required
#android.fix_default_dist = False

# (bool) Allow the application to handle HTTP and HTTPS requests with a self-signed certificate
#android.allow_self_signed_ssl = False

# (bool) Copy the library when there is a changed
#android.copy_libs = True

# (str) The version of the build tools to use
android.build_tools = 33.0.2

# (str) The version of the NDK to use
android.ndk_version = 25.1.8937393

# (bool) Compile the python in the pyc format
#android.pyc = False

# (bool) Compile the python with the debug symbols
#android.pym = False

# (str) The p4a bootstrap to use (one of: sdl2, webview, service_only, pygame, static, )
android.bootstrap = sdl2

# (str) The bootstrap to use (one of: sdl2, webview, service_only, pygame, static, )
#bootstrap = sdl2

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_dir = ../kivy-ios
# Alternately, specify the URL and branch of a git repo:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_dir = ../ios_deploy
# Or specify URL and branch
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# (bool) Whether or not to sign the code
ios.codesign.allowed = false

# (str) Name of the certificate to use for signing
# ios.codesign.certificate =

# (str) The profile to use for signing
# ios.codesign.profile =

#
# Windows specific
#

# (str) SDL2 compiler pkg-config SDL2 mixer pkg-config
#windows.sdl2_lib =
#windows.sdl2_include =
#windows.sdl2_mixer_lib =
#windows.sdl2_mixer_include =

# (bool) Use ANGLE to have OpenGL ES support
#windows.angle = False

# (str) Compiler to use (msvc or mingw)
#windows.compiler = msvc

#
# Requirements
#

# (str) Path to the cython binary (pip install cython, usually automatically)
#cython.bin = cython

# (bool) Ignore requirements when installing
#ignore_requirements = False

#
# Logging
#

# (str) Log level (debug, info, warning, error)
log_level = 2

# (bool) Log to file
#log_to_file = True

# (str) Log file name
#log_filename = buildozer.log

# (bool) Enable logging of the host information
#log_host = True

#
# Buildozer
#

# (int) Maximum number of concurrent threads for build
#jobs = 4

# (str) The directory to look for the Android SDK
#android.sdk_path =

# (str) The directory to look for the Android NDK
#android.ndk_path =

# (str) The directory to look for the Android ANT
#android.ant_path =

# (str) The directory to look for the Android SDK Tools
#android.sdk_tools_path =

# (str) The directory to look for the Android NDK standalone toolchain
#android.ndk_toolchain_path =

# (str) The directory to look for the Android NDK toolchain
#android.toolchain_path =

# (bool) Force the download of the Android SDK
#android.accept_sdk_license = True

# (bool) Force the download of the Android NDK
#android.accept_ndk_license = True

# (bool) Force the download of the Android ANT
#android.accept_ant_license = True

# (bool) Show the commands executed by buildozer
#debug_commands = True

# (bool) Show the debug output of the build
#debug_build = True

# (bool) Run the application in the emulator
#run = False

# (str) The name of the emulator to use
#emulator.name = default

# (str) The avd to use
#emulator.avd = default

# (bool) Start the emulator automatically
#emulator.start = False

# (bool) Wait for the emulator to be ready
#emulator.wait = False

# (int) The timeout for the emulator to be ready
#emulator.timeout = 300

# (str) Extra arguments to pass to the emulator
#emulator.extra_args =

# (str) Extra arguments to pass to the adb
#adb.extra_args =

# (str) The directory to look for the adb
#adb.path =

# (bool) Use the adb from the Android SDK
#adb.use_sdk = True

[buildozer]

# (int) Log level (0 = quiet, 1 = info, 2 = debug)
log_level = 2

# (bool) Warn if the application is built as root
warn_on_root = 1

# (str) Path to the build directory
#build_dir = ./.buildozer

# (str) Path to the bin directory
#bin_dir = ./bin

# (str) Path to the android platform directory
#android_platform_dir = ~/.buildozer/android/platform

# (str) Path to the android SDK directory
#android_sdk_dir = ~/.buildozer/android/platform/android-sdk

# (str) Path to the android NDK directory
#android_ndk_dir = ~/.buildozer/android/platform/android-ndk

# (str) Path to the android ANT directory
#android_ant_dir = ~/.buildozer/android/platform/apache-ant

# (str) Path to the android SDK tools directory
#android_sdk_tools_dir = ~/.buildozer/android/platform/android-sdk/tools

# (str) Path to the android NDK toolchain directory
#android_ndk_toolchain_dir = ~/.buildozer/android/platform/android-ndk/toolchains

# (str) Path to the android NDK standalone toolchain directory
#android_ndk_standalone_dir = ~/.buildozer/android/platform/android-ndk-r25b/toolchains