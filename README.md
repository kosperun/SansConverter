# SansConverter
A stand-alone cross-platform converter for different Sanskrit transliteration systems

### Description
SansConverter is an offline program that allows you to easily and quickly convert transliterated Sanskrit text from one transliteration system to another. You can also type in Sanskrit text in the standard Roman transliteration (IAST) (or other systems) using just your standard QWERTY keyboard.

You can use it to create Sanskrit text with diacritics to use later in online posts, messages, books, articles, etc.  

### SansConverter features:

* Several well-known systems are supported, namely Balaram (1), IAST (2), Harvard-Kyoto (3), Velthuis (4), Cyrillic transliteration both in Russian (5) and Ukrainian (6) versions.
* The text is converted “on the spot” while you are typing or whenever it is pasted into the input window. 
* The program remembers previous transliteration systems that you chose last time and opens them automatically when started next time.
* It also remembers the size of the window (if you resize it) and its position (if you move it on your screen). 
* You can also access all buttons and select transliteration systems with your keyboard, either by pressing Tab or using the shortcuts (Note for Mac OS X users – to use navigation with Tab you first have to go to “System Preferences” and then go to “Keyboard Preferences” and click on Shortcuts” tab and them go to “Accessibility” section and select “all controls” under “Full keyboard access”). 
* You can choose between “ṁ” or “ṃ” by checking the box in the main window (this setting is also remembered at next start).
* Text can be pasted from the clipboard and converted text can be copied to clipboard by pressing the respective buttons. 

NOTE: 
There is a bug when converting from IAST to Balaram (which is caused by the way Balaram system was build) - “ṣ” is converted to “ñ”. Thus, if you convert IAST text like “puruṣa” to Balaram you will get “puruïa” (“puruña”). This is because “ñ” was also used in Balaram and thus it gets converted wrongly. Since Balaram is a legacy system and I don’t know if many people will use this program to convert IAST text to Balaram, I decided to save time and to leave this as it is for now. The workaround for such little problem is to first convert from IAST to any other system (preferably Velthuis because it allows capital letters) and then use “Swap transliterations and texts” button and select Balaram as the target transliteration. 

### INSTALLATION:

SansConverter comes in two editions: 
- the **main version** (v1.6, with version number without any suffix) is all-Unicode and works with the six transliteration systems mentioned above. This edition is for everyone who works with Roman or Cyrillic Unicode transliteration of Sanskrit texts and doesn't need the custom BBT font called "Gaura Times".
- the **"Gaura Times edition"** (v1.6gt) has a "gt" suffix in the version number and has an additional transliteration system called "Gaura Times". It is a custom system, developed by the Russian BBT, which is not represented in the Unicode tables and therefore cannot be used online without setting your custom font on a webpage. It is widely used in BBT publications and online Vedabase that make use of Cyrillic alphabet. Another difference between the main version and the "gt" version is that the output window for the transliterated text is set to the "Gaura Times" serif font for all transliterations systems. This edition will be useful only for those who work with the "Gaura Times" font.

The program requires no installation and you can just drag and drop the .exe or .app file to your Panel in Windows or to your Application folder or Dock on Mac.

**macOS note:** When opening the app for the first time, macOS may show a warning that it cannot verify the app. This is because the app is not signed with an Apple Developer certificate. To open it anyway:
1. Try to open the app — click **Done** when the warning appears.
2. Go to **System Settings → Privacy & Security**.
3. Scroll down and click **Open Anyway** next to the SansConverter entry.

Alternatively, run this command in Terminal:
```
xattr -dr com.apple.quarantine /path/to/SansConverter.app
```

There is some more information about transliteration systems under “Help” menu. 

You can also send your feedback or reports to the address given in the “About” menu. 

### SansConverter in action
#### part 1
![image](https://user-images.githubusercontent.com/68146217/182867782-faad4e8c-598f-431d-9da4-5193ca0fd7ea.png)

#### part 2
![image](https://user-images.githubusercontent.com/68146217/182867851-186603ab-0bea-4a8b-9b03-3608b9f5530d.png)

#### part 3
![image](https://user-images.githubusercontent.com/68146217/182867915-54d98757-79b0-45d4-ba61-8a6b45a57fe4.png)
