# BiG-Kelz Android App

A WebView-based Android application that loads a local web server interface. This app provides a native Android wrapper around a web application running on `http://127.0.0.1:8000`.

## 🚀 Features

- **WebView Integration**: Seamlessly displays web content in a native Android app
- **JavaScript Enabled**: Full support for dynamic web content and interactions
- **Local Server Support**: Designed to work with local backend servers
- **Modern Android Architecture**: Built with AndroidX and Material Design components

## �� Requirements

- **Minimum SDK**: Android 5.0 (API 21)
- **Target SDK**: Android 13 (API 33)
- **Java Version**: 17
- **Gradle Version**: 8.0.2
- **Android Gradle Plugin**: 8.0.0

## 🛠️ Build Setup

### Prerequisites

1. **Android Studio** (recommended) or command line tools
2. **Java 17** JDK
3. **Android SDK** with API 33

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd big_kelz_pro_max_full
   ```

2. **Open in Android Studio**:
   - Open Android Studio
   - Select "Open an existing project"
   - Navigate to the `android` folder and open it

3. **Build the project**:
   ```bash
   cd android
   ./gradlew assembleDebug
   ```

4. **Install on device**:
   ```bash
   ./gradlew installDebug
   ```

### Command Line Build

```bash
# Navigate to android directory
cd android

# Build debug APK
gradle assembleDebug

# Build release APK
gradle assembleRelease
```

## ��️ Project Structure

```
android/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/
│   │       │       └── bigkelz/
│   │       │           └── app/
│   │       │               └── MainActivity.java
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   │   └── activity_main.xml
│   │       │   └── values/
│   │       │       └── strings.xml
│   │       └── AndroidManifest.xml
│   ├── build.gradle
│   └── proguard-rules.pro
├── build.gradle
├── settings.gradle
├── gradle.properties
└── gradle/
    └── wrapper/
        └── gradle-wrapper.properties
```

##  Configuration

### Web Server URL

The app is configured to load `http://127.0.0.1:8000` by default. To change this:

1. Open `android/app/src/main/java/com/bigkelz/app/MainActivity.java`
2. Modify line 22:
   ```java
   webView.loadUrl("http://your-server-url:port");
   ```

### Build Configuration

Key build settings in `android/app/build.gradle`:

```gradle
android {
    namespace 'com.bigkelz.app'
    compileSdk 33
    
    defaultConfig {
        applicationId "com.bigkelz.app"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }
}
```

## 🚀 CI/CD Pipeline

This project includes GitHub Actions for automated builds:

### Workflow Features

- **Automatic Builds**: Triggers on pushes to `main` branch
- **Java 17**: Uses Temurin JDK 17
- **Gradle 8.0.2**: Compatible with Android Gradle Plugin 8.0.0
- **Android SDK**: Automated setup with API 33
- **Artifact Upload**: Builds are saved as GitHub artifacts

### Manual Trigger

You can manually trigger builds from the GitHub Actions tab in your repository.

## 📦 Dependencies

### Core Dependencies

- **AndroidX AppCompat**: `1.6.1` - Backward compatibility
- **Material Design**: `1.8.0` - Modern UI components
- **ConstraintLayout**: `2.1.4` - Flexible layouts

### Build Dependencies

- **Android Gradle Plugin**: `8.0.0`
- **Gradle**: `8.0.2`
- **Java**: `17`

## 🔒 Permissions

The app requires the following permissions (defined in `AndroidManifest.xml`):

- **Internet Access**: Required for WebView to load web content
- **Network State**: For network connectivity checks

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Ensure Java 17 is installed
   - Verify Android SDK API 33 is available
   - Check Gradle version compatibility

2. **WebView Issues**:
   - Ensure your web server is running on the configured URL
   - Check network connectivity
   - Verify JavaScript is enabled (already configured)

3. **Permission Issues**:
   - Grant internet permissions if prompted
   - Check device network settings

### Debug Mode

Enable debug logging by adding to `MainActivity.java`:

```java
if (BuildConfig.DEBUG) {
    Log.d("MainActivity", "Loading URL: " + url);
}
```

##  License

[Add your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the build logs for specific error messages

---

**Note**: This app requires a running web server on `http://127.0.0.1:8000` to function properly. Ensure your backend service is running before launching the app.
```

This README provides comprehensive documentation for your Android project, including build instructions, project structure, configuration options, and troubleshooting tips. You can customize it further based on your specific needs and add any additional sections that might be relevant to your project.
