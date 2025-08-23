BiG Kelz PRO MAX - Full package (MT5 live + APK + Server CI)

What's inside:
- Full MT5 adapter (core/brokers/mt5_live.py) - requires MetaTrader5 Python package and MT5 terminal on Windows.
- Executor, session manager, control endpoints, signals, trade router.
- Static PWA UI for quick controls.
- Dockerfile to build server image.
- GitHub Actions workflow .github/workflows/ci.yml that builds the Android APK and builds/pushes the Docker image (requires DockerHub secrets).
- Android project zip may be included as android_project.zip (open in Android Studio to customize webview URL).

How to use:
1. Place MT5 terminal on Windows VPS, install Python and MetaTrader5 package.
2. Configure repo and push to GitHub (your account). Add DockerHub secrets DOCKERHUB_USERNAME and DOCKERHUB_TOKEN.
3. On GitHub: Actions -> run Workflow or push to main to trigger CI. APK artifact available under Actions artifacts. Docker image pushed to DockerHub under your account.
4. Deploy Docker image to your VPS or run locally.
Notes:
- Replace placeholder core files with full strategy code provided earlier in the chat (config, utils, features, signal_engine, etc.) if not already included.
- Test extensively on demo before using live accounts.
