
<p align="center">
  <img src="docs/public/assets/logo/logo.png" style="display: block; margin: 0 auto;" width="700"/>
</p>

# Aether: Your Digital Webcam Sentinel

Aether is an open-source software designed with privacy in mind. It logs computer logins, captures images, and encrypts and stores them locally. Aether ensures complete privacy by not transmitting any data or metadata, operating entirely on your local machine.

> Note: Aethr is still in development and is now in *pre-release*.

## Features

- **Secure Local Capture**: Automatically captures photos during login and stores them securely on your local machine.
- **Advanced Encryption**: Strong encryption ensures your data remains private and protected.
- **Private Data Storage**: No data is transmitted; all information is stored locally with no external servers involved.
- **Comprehensive Activity Logging**: Track all application events and actions for complete transparency.
- **Fully Customizable Settings**: Control your privacy and security settings, and configure the application to suit your needs.

## Detailed Features

### Camera Configuration
- **Choose Camera**: Select your preferred camera from the available list.
- **Camera Test**: Test your camera to ensure it functions correctly.
- **Save Preference**: Save your camera preference for future use.

### Storage Settings
- **Select Location**: Choose where you want to save the captured photos (default: User/Pictures/Aether).
- **Browse and Confirm**: Use the Browse button to select your preferred storage location, then confirm with the Save button.

### Security Features
- **Auto-Start**: Automatically begins the capture process upon login.
- **Encryption**: Captures are encrypted using a password of your choice to secure your images.
- **Compression**: Images are compressed to save space while retaining quality.
- **Logging**: Aether tracks all events and actions within the application for better visibility and control.

### Password Management
- **Set Secure Password**: Ensure the security of your captured data by setting a strong password.
- **Avoid Special Characters**: To prevent issues, avoid non-ASCII characters in passwords (e.g., ü, ğ, ı, ê, æ, ß).

### Advanced Settings
- **Task Scheduler**: Customize Aether’s behavior using Task Scheduler. You can set conditions, such as starting the capture process when a specific application is launched.

### Known Issues
- **Encryption Only Mode**: If only encryption is enabled in the config, images will neither be encrypted nor compressed.
- **Splash Screen Delay**: A brief delay after the splash screen is normal due to the OpenCV camera detection process.

## Installation

1. **Download**: Get the latest version from the [releases](https://github.com/enesehs/aether/releases) page. or download at [Aether Website](https://enesehs.me/Aether) 
2. **Install**: Install `AetherSetup.exe` Choose install location and launch
3. **Run**: Launch Aether by running `Aether.exe`. as Administrator

## Usage

1. **Launch Aether**: Open the application.
2. **Configure Settings**: Adjust your camera and storage settings.
3. **Activate Capture**: Enable the auto-start feature and configure the encryption and compression settings.
4. **Start Logging**: The app will automatically capture and log events as configured.

## Contact

For feedback, bug reports, or support, contact [enesehs@protonmail.com](mailto:enesehs@protonmail.com).

## License

Aether is licensed under the [GNU 4](LICENSE).


