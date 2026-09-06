---
name: web-to-mobile-apk
description: Use when building Android APK from websites or web apps.
version: 1.0.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [android, apk, webview, mobile, github-actions, gradle]
    category: software-development
---

# Web-to-Mobile APK Generation

Build and package responsive websites or Single-Page Applications (SPAs) into standalone, installable Android APKs using a native WebView wrapper built via GitHub Actions or local Gradle.

## Architecture

A production-ready WebView wrapper requires:
- **`MainActivity`**: Configures `WebView`, `SwipeRefreshLayout`, and `ProgressBar`.
- **`WebSettings`**: Enables JavaScript, DOM storage, database, and custom user-agent.
- **`WebViewClient`**: Keeps internal navigation in-app and delegates external domains to system browser.
- **Back Navigation**: Intercepts `KEYCODE_BACK` to navigate web history before exiting.
- **CI/CD Build Runner**: Uses GitHub Actions to compile without requiring local multi-gigabyte Android SDK installations.

## Procedure

### 1. Scaffold Android Project Structure

Create the project directory tree (typically under `~/Website/<app-name>-mobile`):

```bash
mkdir -p app/src/main/java/com/<org>/<app>
mkdir -p app/src/main/res/values
mkdir -p app/src/main/res/layout
mkdir -p app/src/main/res/mipmap-{hdpi,mdpi,xhdpi,xxhdpi,xxxhdpi}
mkdir -p gradle/wrapper .github/workflows
```

### 2. Configure Manifest and WebView Settings

In `app/src/main/AndroidManifest.xml`:
- Request permissions: `android.permission.INTERNET` and `android.permission.ACCESS_NETWORK_STATE`.
- Target API 34, Min SDK 24.
- Do NOT declare `package="com.domain.app"` in the manifest root; declare `namespace` in `app/build.gradle` (AGP 8+ requirement).

In `MainActivity.java`:
- Enable DOM storage: `settings.setDomStorageEnabled(true)` (mandatory for localStorage/token persistence in SPAs like Vue, React, Next.js).
- Enable Database storage: `settings.setDatabaseEnabled(true)`.
- Enable JavaScript: `settings.setJavaScriptEnabled(true)`.
- Configure `WebViewClient.shouldOverrideUrlLoading`: return `false` for target domain, launch `Intent.ACTION_VIEW` for external links.
- Override `onKeyDown`:
  ```java
  @Override
  public boolean onKeyDown(int keyCode, KeyEvent event) {
      if (keyCode == KeyEvent.KEYCODE_BACK && webView.canGoBack()) {
          webView.goBack();
          return true;
      }
      return super.onKeyDown(keyCode, event);
  }
  ```

### 3. Generate Clean App Launcher Icons

Generate standalone PNG launcher icons without external dependencies using Python stdlib (`zlib`, `struct`):
- Avoid neon or generic templates; adhere to clean, light-themed palettes (soft pink `#F472B6` / clean white).
- Write `ic_launcher.png` and `ic_launcher_round.png` into each `res/mipmap-*/` directory (`mdpi`: 48px, `hdpi`: 72px, `xhdpi`: 96px, `xxhdpi`: 144px, `xxxhdpi`: 192px).
- When the user provides a custom image file (e.g. photo or illustration):
  1. Use `ffmpeg -i <src> -vf scale=<size>:<size> -f rawvideo -pix_fmt rgba -` to stream raw RGBA bytes into Python.
  2. For `ic_launcher.png`, calculate a 20% corner-radius mask (rounded rectangle).
  3. For `ic_launcher_round.png`, calculate a circular radius mask (`dist <= size/2`).
  4. Encode via PNG chunks (`IHDR`, `IDAT`, `IEND`) using `zlib.compress` to bypass missing Pillow/PIL modules.

### 4. Build Configuration (Gradle & AGP)

In `build.gradle`:
```groovy
plugins {
    id 'com.android.application' version '8.2.2' apply false
}
```

In `app/build.gradle`:
```groovy
plugins {
    id 'com.android.application'
}

android {
    namespace 'com.<org>.<app>'
    compileSdk 34

    defaultConfig {
        applicationId "com.<org>.<app>"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            signingConfig signingConfigs.debug // Auto-sign with debug key for instant sideloading
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.11.0'
    implementation 'androidx.swiperefreshlayout:swiperefreshlayout:1.1.0'
}
```

In `settings.gradle`:
```groovy
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "<App>"
include ':app'
```

### 5. Build Automation via GitHub Actions

When host VPS lacks OpenJDK or Android build tools:
1. Initialize git and commit:
   ```bash
   git init && git branch -M main && git add . && git commit -m "Initial commit"
   ```
2. Create and push private repo via GitHub CLI:
   ```bash
   gh repo create <repo-name> --private --source=. --remote=origin --push
   ```
3. In `.github/workflows/build-apk.yml`:
   ```yaml
   name: Build APK
   on: [push, workflow_dispatch]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: actions/setup-java@v4
           with:
             java-version: '17'
             distribution: 'temurin'
         - uses: gradle/actions/setup-gradle@v3
           with:
             gradle-version: '8.5' # Pin Gradle 8.5 for AGP 8.2 compatibility
         - run: gradle assembleRelease
         - uses: actions/upload-artifact@v4
           with:
             name: <App>-app
             path: app/build/outputs/apk/release/*.apk
   ```
4. Watch build execution:
   ```bash
   gh run watch <RUN_ID> --interval 10 --exit-status
   ```
5. Download and stage artifact:
   ```bash
   gh run download <RUN_ID> -R <owner>/<repo> -n <App>-app -D /dest/path
   ```

## Pitfalls

- **Do NOT omit DOM storage in WebSettings**: Modern SPAs rely on `localStorage` or `sessionStorage` for auth JWTs and user state. Without `setDomStorageEnabled(true)`, authentication cookies and sessions vanish on reload, trapping users on the login screen.
- **Pin Gradle 8.5 for AGP 8.2.2**: Gradle 9+ introduces breaking API restrictions that fail Android resource processing (`Cannot mutate the dependencies of configuration after resolved`). Explicitly pass `gradle-version: '8.5'` to `gradle/actions/setup-gradle@v3`.
- **Remove package attribute from AndroidManifest.xml**: AGP 8+ deprecates setting package in AndroidManifest. Leaving `package="com..."` in manifest produces build warnings and causes namespace collisions with `namespace` in `build.gradle`.
- **Auto-sign release builds for sideloading**: Unsigned APKs cannot be installed on standard Android devices without manual zipalign and apksigner. Assign `signingConfig signingConfigs.debug` to the `release` build type so `assembleRelease` produces an instantly installable APK.
- **Always bump versionCode on asset/code changes**: Android Package Manager caches existing installed packages and ignores reinstallations if `versionCode` matches the already installed version. Increment `versionCode` (e.g. 1 -> 2) and `versionName` (e.g. 1.0.0 -> 1.0.1) in `app/build.gradle` on every rebuild.
- **Deliver APK natively to Telegram via MEDIA tag**: Return `MEDIA:/absolute/path/to/<App>.apk` so the messaging platform delivers the binary directly as a tappable native download attachment.
- **Internal vs External navigation routing**: Always check the URL prefix in `shouldOverrideUrlLoading`. Returning `false` for your domain keeps navigation in-app; launching `Intent.ACTION_VIEW` for other domains allows social login (Google, GitHub) or documentation links to open safely in the external browser.
