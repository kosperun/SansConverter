"""Select Encodings dialog window"""

from PyQt6.QtCore import QCoreApplication, Qt
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from windows.select_encodings_warning import WarningDialog


class UiSelectEncodingsDialog(QDialog):
    """Enable/Disable and reorder encodings GUI"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent_dialog = parent
        self.setObjectName("Dialog")
        self.resize(300, 280)
        self.setWindowTitle(QCoreApplication.translate("Dialog", "Select encodings", None))

        self.mainLayout = QVBoxLayout(self)

        self.label = QLabel("Check encodings to enable them. Drag to reorder.", self)
        self.mainLayout.addWidget(self.label)

        self.listWidget = QListWidget(self)
        self.listWidget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.listWidget.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.mainLayout.addWidget(self.listWidget)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        self.mainLayout.addWidget(self.buttonBox)

        self._populate_list()

        self.buttonBox.accepted.connect(self.check_selected_encodings)
        self.buttonBox.rejected.connect(self.reject)

    def _populate_list(self):
        # Show selected encodings first (in their saved order), then unselected ones
        selected = self.parent_dialog.selected_encodings
        unselected = [e for e in self.parent_dialog.all_encodings if e not in selected]

        for encoding in selected + unselected:
            item = QListWidgetItem(encoding)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if encoding in selected else Qt.CheckState.Unchecked)
            self.listWidget.addItem(item)

    def get_selected_encodings(self):
        return [
            self.listWidget.item(i).text()
            for i in range(self.listWidget.count())
            if self.listWidget.item(i).checkState() == Qt.CheckState.Checked
        ]

    def check_selected_encodings(self):
        selected_encodings = self.get_selected_encodings()
        if not selected_encodings:
            warning_dialog = WarningDialog(self)
            if warning_dialog.exec() == QDialog.DialogCode.Accepted:
                # Check all items so get_selected_encodings() returns them in list order
                for i in range(self.listWidget.count()):
                    self.listWidget.item(i).setCheckState(Qt.CheckState.Checked)
                self.accept()
            # Rejected = Go Back, stay open
        else:
            self.accept()
