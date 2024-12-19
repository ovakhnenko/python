import sys
import subprocess
from PyQt5 import QtWidgets

class UserGenerator(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.defaultPassword = "123Start#"
        self.userOU = "OU=Users,OU=TEST,DC=test,DC=local"  
        self.groupOU = "OU=Groups,OU=TEST,DC=test,DC=local"
        self.domainName = "test.local"
        
        self.init_ui()
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        
        self.scrollable_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scrollable_widget)
        
        self.form_layout = QtWidgets.QGridLayout(self.scrollable_widget)
        
        self.button_generiere = QtWidgets.QPushButton("Generiere", self)
        self.button_generiere.clicked.connect(self.on_generiere_button_click)
        self.button_generiere.setStyleSheet("background-color: blue; color: white;")
        self.form_layout.addWidget(self.button_generiere, 0, 1)
        
        self.button_standardwert = QtWidgets.QPushButton("Standardwert", self)
        self.button_standardwert.clicked.connect(self.on_default_button_click)
        self.form_layout.addWidget(self.button_standardwert, 0, 2)
        
        self.button_schliessen = QtWidgets.QPushButton("Schließen", self)
        self.button_schliessen.clicked.connect(self.close)
        self.form_layout.addWidget(self.button_schliessen, 0, 3)
        
        self.userOU_input = self.create_input_field("Benutzer OU", self.userOU, 1, "color: black;")
        self.groupOU_input = self.create_input_field("Gruppe OU", self.groupOU, 2, "color: black;")
        self.domainName_input = self.create_input_field("Domänename", self.domainName, 3, "black: blue;")
        
        self.vorname_input = self.create_input_field("Benutzervorname", "", 4, "color: blue;", self.on_name_aendert)
        self.nachname_input = self.create_input_field("Benutzernachname", "", 5, "color: blue;", self.on_name_aendert)
        self.defaultPassword_input = self.create_input_field("Benutzerkennwort", self.defaultPassword, 6, "color: black;")
        self.userName_input = self.create_input_field("Benutzername", "", 7, "color: black;")
        self.email_input = self.create_input_field("E-Mail", "", 8, "color: black;")
        
        self.groups = ["group 1", "group 2", "group 3", "group 4", "group 5", "group 6", "group 1", "group 2", "group 3", "group 4", "group 5", "group 6"]
        self.var_list = []
        
        for i, group in enumerate(self.groups):
            checkbox = QtWidgets.QCheckBox(group, self)
            self.form_layout.addWidget(checkbox, 9 + i, 0, 1, 4)
            self.var_list.append(checkbox)
        
        layout.addWidget(self.scroll_area)
        
        self.standardwertenEinstellen()
        
    def create_input_field(self, label_text, default_value, row, LabelStyle, callback=None):
        label = QtWidgets.QLabel(label_text, self)
        label.setStyleSheet(LabelStyle)
        self.form_layout.addWidget(label, row, 1)
        input_field = QtWidgets.QLineEdit(self)
        input_field.setText(default_value)
        if callback:
            input_field.textChanged.connect(callback)
        self.form_layout.addWidget(input_field, row, 2)
        return input_field
        
    def on_name_aendert(self):
        userName = f"{self.vorname_input.text().lower()}.{self.nachname_input.text().lower()}"
        emailAddress = f"{userName}@{self.domainName_input.text()}"
        self.userName_input.setText(userName)
        self.email_input.setText(emailAddress)
        self.pruefe_daten()
    
    def pruefe_daten(self):
        if len(self.userName_input.text()) > 20:
            self.button_generiere.setEnabled(False)
        else:    
            self.button_generiere.setEnabled(True)
    
    def on_generiere_button_click(self):
        groupOU = self.groupOU_input.text()
        ps_command = f"Get-ADGroup -Filter * -SearchBase {groupOU} | Select-Object Name"
        result = self.ps_run(ps_command)
        print(result)
    
    def on_default_button_click(self):
        self.standardwertenEinstellen()
    
    def ps_run(self, ps_command):
        completed = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
        return completed.stdout
    
    def standardwertenEinstellen(self):
        self.userOU_input.setText(self.userOU)
        self.groupOU_input.setText(self.groupOU)
        self.domainName_input.setText(self.domainName)
        self.vorname_input.setText("")
        self.nachname_input.setText("")
        self.defaultPassword_input.setText(self.defaultPassword)
        self.userName_input.setText("")
        self.email_input.setText("")
    
    def get_selected_groups(self):
        selected_groups = [group.text() for i, group in enumerate(self.var_list) if group.isChecked()]
        print(selected_groups)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UserGenerator()
    window.setWindowTitle("Benutzergenerator")
    window.resize(800, 600)
    window.vorname_input.setFocus()
    window.show()
    sys.exit(app.exec_())
