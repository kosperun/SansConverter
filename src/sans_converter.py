"""The main module for the app logic"""

import sys

from PyQt6 import QtCore, QtWidgets

from encoding_mappings import (
    ALL_EXT_ENCODINGS,
    CYRILLIC_ENCODINGS,
    HK,
    HK_EXT,
    ROMAN_BASIC_ENCODINGS,
    Encodings,
)
from service import convert
from windows.about import UiAboutDialog
from windows.converter import Ui_SansConverter
from windows.help import UiHelpDialog
from windows.select_encodings import UiSelectEncodingsDialog

# Encoding display names saved to QSettings under old versions of the app.
# Applied on load so existing users' saved encoding selections carry over
# instead of silently disappearing after the rename.
RENAMED_ENCODINGS = {
    "Cyrillic (Ukrainian)": Encodings.UKR_G.value,
    "Cyrillic (Russian)": Encodings.RUS.value,
}


class SansConverter(QtWidgets.QMainWindow):
    """This is the main class with all the logic and connections between the GUI parts and class methods"""

    settings = QtCore.QSettings("Kos Perun", "SansConverter")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_SansConverter()
        self.ui.setupGUi(self)
        self.setWindowFlags(QtCore.Qt.WindowType.Window)

        self.all_encodings = [item.value for item in Encodings]
        # Read saved settings for "Use ṃ", original and target encodings, window
        # size and position:
        self.selected_encodings = self.settings.value("selected_encodings", [])
        self.selected_encodings = [RENAMED_ENCODINGS.get(e, e) for e in self.selected_encodings]

        if not self.selected_encodings:
            self.selected_encodings = self.all_encodings
            self.open_select_encodings()
        else:
            self.update_comboboxes()

        input_encoding_name = RENAMED_ENCODINGS.get(
            self.settings.value("input_encoding_name"), self.settings.value("input_encoding_name")
        )
        output_encoding_name = RENAMED_ENCODINGS.get(
            self.settings.value("output_encoding_name"), self.settings.value("output_encoding_name")
        )
        self.ui.comboBox.setCurrentText(input_encoding_name)
        self.ui.comboBox_2.setCurrentText(output_encoding_name)
        self.ui.checkBox.setChecked(self.settings.value("Use m", type=bool))
        self.resize(self.settings.value("WindowSize", QtCore.QSize(620, 550)))
        self.move(self.settings.value("Position", QtCore.QPoint(600, 230)))
        # Linking buttons, hotkeys and menus to functions
        self.ui.pushButton.clicked.connect(self.copy_converted)
        self.ui.pushButton_2.clicked.connect(self.swap_encodings)
        self.ui.pushButton_3.clicked.connect(self.clear_input)
        self.ui.pushButton_4.clicked.connect(self.paste_input)
        # Convert on the go when input_encoding_name is changed manually and
        # remember it (save it to external file) to use when
        # the program is started again
        self.ui.comboBox.currentIndexChanged.connect(self.convert)
        # Convert on the go when output_encoding_name is changed manually and
        # remember it (save it to external file) to use when
        # the programs is started again
        self.ui.comboBox_2.currentIndexChanged.connect(self.convert)
        # Converts on the go while typing text into textEdit widget
        self.ui.textEdit.textChanged.connect(self.convert)
        # Converts again whenever "Use "ṃ"" is checked or unchecked
        self.ui.checkBox.stateChanged.connect(self.convert)
        self.ui.actionClear.triggered.connect(self.clear_input)
        self.ui.actionCopy.triggered.connect(self.copy_converted)
        self.ui.actionPaste.triggered.connect(self.paste_input)
        self.ui.actionRedo.triggered.connect(self.ui.textEdit.redo)
        self.ui.actionUndo.triggered.connect(self.ui.textEdit.undo)
        self.ui.actionQuit.triggered.connect(self.close)
        self.ui.actionSwap.triggered.connect(self.swap_encodings)
        self.ui.actionSelect_encodings.triggered.connect(self.open_select_encodings)
        self.ui.actionTransliteration_help.triggered.connect(self.open_help)
        self.ui.actionAbout_SansConverter.triggered.connect(self.open_about)
        self.show()

    def clear_input(self):
        """
        Clears the input window (and undoes history!)
        """
        self.ui.textEdit.clear()

    def paste_input(self):
        """
        Paste text from clipboard into the input window
        """
        self.ui.textEdit.paste()

    def open_help(self):
        """
        Opens a dialog window with help in it
        """
        dialog = UiHelpDialog(self)
        dialog.show()
        dialog.adjustSize()

    def open_about(self):
        """
        Opens a dialog window with 'About' information
        """
        dialog = UiAboutDialog(self)
        dialog.show()
        dialog.adjustSize()

    def open_select_encodings(self):
        """
        Opens a dialog window with selection of available encodings
        """
        dialog = UiSelectEncodingsDialog(self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.selected_encodings = dialog.get_selected_encodings()
        # Cancelled: keep previously selected encodings unchanged
        self.update_comboboxes()

    def update_comboboxes(self):
        self.ui.comboBox.blockSignals(True)
        self.ui.comboBox_2.blockSignals(True)

        self.ui.comboBox.clear()
        self.ui.comboBox_2.clear()
        self.ui.comboBox.addItems(self.selected_encodings)
        self.ui.comboBox_2.addItems(self.selected_encodings)

        self.ui.comboBox.blockSignals(False)
        self.ui.comboBox_2.blockSignals(False)

    def convert(self) -> None:
        """
        Selects the appropriate character tables and sends them to the 'convert' method.
        ROMAN_BASIC_ENCODINGS uses short lists with only diacritical letters for Roman↔Roman conversion.
        ALL_EXT_ENCODINGS uses full alphabet lists for any conversion involving Cyrillic.
        HK is a special case because it uses only lowercase letters.
        """
        text = self.ui.textEdit.toPlainText()
        input_encoding_name = self.ui.comboBox.currentText()
        output_encoding_name = self.ui.comboBox_2.currentText()

        # To save time for identical encodings we don't convert them
        if input_encoding_name != output_encoding_name:
            # Peculiarities of the HK scheme, it uses only lowercase letters
            if output_encoding_name == Encodings.HK.value:
                if input_encoding_name not in CYRILLIC_ENCODINGS and text.islower():
                    input_chars = ROMAN_BASIC_ENCODINGS[input_encoding_name]
                    output_chars = HK
                else:
                    input_chars = ALL_EXT_ENCODINGS[input_encoding_name]
                    output_chars = HK_EXT
                    text = text.lower()

            # Simplify transliteration of the similar encodings that are based on Roman script
            elif input_encoding_name in ROMAN_BASIC_ENCODINGS and output_encoding_name in ROMAN_BASIC_ENCODINGS:
                input_chars = ROMAN_BASIC_ENCODINGS[input_encoding_name]
                output_chars = ROMAN_BASIC_ENCODINGS[output_encoding_name]

            # For transliterating between Roman and Cyrillic transliterations
            else:
                input_chars = ALL_EXT_ENCODINGS[input_encoding_name]
                output_chars = ALL_EXT_ENCODINGS[output_encoding_name]

            text = convert(
                text,
                input_chars,
                output_chars,
                input_encoding_name,
                output_encoding_name,
                change_anusvara=self.ui.checkBox.isChecked(),
            )
        self.ui.textBrowser.setPlainText(text)

    def copy_converted(self) -> None:
        """
        Copies converted text from the output window when the 'Copy' button is pressed
        """
        self.ui.textBrowser.selectAll()
        self.ui.textBrowser.copy()

    def swap_encodings(self) -> None:
        """
        Pastes converted text from the output window, swaps encodings
        and converts the text back into original encoding
        """
        output = self.ui.textBrowser.toPlainText()
        enc1 = self.ui.comboBox.currentText()
        enc2 = self.ui.comboBox_2.currentText()
        self.ui.comboBox.setCurrentText(enc2)
        self.ui.comboBox_2.setCurrentText(enc1)
        self.ui.textEdit.setPlainText(output)

    def closeEvent(self, event) -> None:
        """
        Remembers settings and quits the program
        """
        self.settings.setValue("input_encoding_name", self.ui.comboBox.currentText())
        self.settings.setValue("output_encoding_name", self.ui.comboBox_2.currentText())
        self.settings.setValue("Use m", self.ui.checkBox.isChecked())
        self.settings.setValue("WindowSize", self.size())
        self.settings.setValue("Position", self.pos())
        self.settings.setValue("selected_encodings", self.selected_encodings)


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = SansConverter()  # noqa
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
