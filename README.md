# SansConverter
A stand-alone cross-platform converter for different Sanskrit transliteration systems

### Description
SansConverter is an offline program that allows you to easily and quickly convert transliterated Sanskrit text from one transliteration system to another. You can also type in Sanskrit text in the standard Roman transliteration (IAST) (or other systems) using just your standard QWERTY keyboard.

You can use it to create Sanskrit text with diacritics to use later in online posts, messages, books, articles, etc.

### SansConverter features:

* Seven transliteration systems are supported: **IAST**, **Balaram**, **Harvard-Kyoto**, **Velthuis**, **Cyrillic (Ukrainian)**, **Cyrillic (Russian)**, and **Gaura Times** — a legacy non-Unicode Cyrillic system developed by the Russian ISKCON BBT, used in their publications and requiring a custom font of the same name.
* Text is converted in real time as you type or paste into the input field.
* You can choose between "ṁ" (dot above) or "ṃ" (dot below) for the anusvara via a checkbox in the main window.
* The program remembers your previously selected transliteration systems, window size, window position, anusvara style, and enabled encodings — all restored automatically on next launch.
* You can enable or disable individual transliteration systems via **Settings → Enable/Disable encodings** in the menu. You can also **reorder** them by dragging and dropping in that dialog — only the systems you need will appear in the dropdowns.
* All major functions have keyboard shortcuts; you can also navigate between controls using Tab.
* Text can be pasted from the clipboard and converted text can be copied to the clipboard via buttons or keyboard shortcuts.

**Keyboard shortcuts:**

| Action | Shortcut |
|---|---|
| Paste from clipboard | Ctrl+V |
| Copy converted text | Ctrl+C |
| Clear input | Ctrl+R |
| Swap transliterations and texts | Alt+S |
| Undo | Ctrl+Z |
| Redo | Ctrl+Y |
| Quit | Ctrl+Q |

### Typing Sanskrit with a standard keyboard

SansConverter can also be used as a typing aid. Both **Harvard-Kyoto** and **Velthuis** are pure ASCII systems — every character is typeable on a standard QWERTY keyboard with no special input methods or keyboard layouts required.

To type Sanskrit text with diacritics:
1. Select Harvard-Kyoto or Velthuis as the input system and your desired output (e.g. IAST) as the output system.
2. Type your text in the input field using the ASCII notation.
3. The converted text with proper diacritics appears instantly in the output field — copy it from there.

**Harvard-Kyoto** example: type `kRSNa` → get `kṛṣṇa`

**Velthuis** example: type `k.r.s.na` → get `kṛṣṇa`

Velthuis has the advantage of supporting capital letters, making it suitable for text that mixes uppercase and lowercase. Full character schemas for both systems are available under the **Help** menu in the app.

More details on Wikipedia:
- Harvard-Kyoto: https://en.wikipedia.org/wiki/Harvard-Kyoto
- Velthuis: https://en.wikipedia.org/wiki/Velthuis

### Installation

Download the latest release for your platform from the [Releases page](https://github.com/kosperun/SansConverter/releases):

- **Windows:** download `SansConverter.exe` and run it. You can pin it to your Taskbar for easy access.
- **macOS:** download the `.dmg`, open it, and drag the app to your Applications folder or Dock.
- **Linux (Debian/Ubuntu):** download the `.deb` and install it with `sudo dpkg -i SansConverter.deb`.
- **Linux (other distributions):** download the `.tar.gz`, extract it, and run the `SansConverter` binary.

No further installation is required.

**macOS note:** When opening the app for the first time, macOS may show a warning that it cannot verify the app. This is because the app is not signed with an Apple Developer certificate. To open it anyway:
1. Try to open the app — click **Done** when the warning appears.
2. Go to **System Settings → Privacy & Security**.
3. Scroll down and click **Open Anyway** next to the SansConverter entry.

Alternatively, run this command in Terminal:
```
xattr -dr com.apple.quarantine /path/to/SansConverter.app
```

**macOS keyboard navigation:** To use Tab for navigating between controls, go to **System Settings → Keyboard** and enable **"Use keyboard navigation to move focus between controls"**.

More information about each transliteration system is available under the **Help** menu. You can send feedback or bug reports directly from the **About** menu.

### SansConverter in action

![image](https://user-images.githubusercontent.com/68146217/182867782-faad4e8c-598f-431d-9da4-5193ca0fd7ea.png)

![image](https://user-images.githubusercontent.com/68146217/182867851-186603ab-0bea-4a8b-9b03-3608b9f5530d.png)

![image](https://user-images.githubusercontent.com/68146217/182867915-54d98757-79b0-45d4-ba61-8a6b45a57fe4.png)
