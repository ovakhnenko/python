import sys
import msvcrt
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

        #buttons        
        self.button_generiere = QtWidgets.QPushButton("Generiere", self)
        self.button_generiere.clicked.connect(self.on_generiere_button_click)
        self.form_layout.addWidget(self.button_generiere, 0, 1)
        
        self.button_standardwert = QtWidgets.QPushButton("Standardwert", self)
        self.button_standardwert.clicked.connect(self.on_default_button_click)
        self.form_layout.addWidget(self.button_standardwert, 0, 2)
        
        self.button_schliessen = QtWidgets.QPushButton("Schließen", self)
        self.button_schliessen.clicked.connect(self.close)
        self.form_layout.addWidget(self.button_schliessen, 0, 3)

        #daten       
        self.userOU_input = self.create_input_field("Benutzer OU", self.userOU, 1, "color: black;")
        self.groupOU_input = self.create_input_field("Gruppe OU", self.groupOU, 2, "color: black;")
        self.domainName_input = self.create_input_field("Domänename", self.domainName, 3, "color: black;")
        
        self.vorname_input = self.create_input_field("Benutzervorname", "", 4, "color: blue;", self.on_name_aendert)
        self.nachname_input = self.create_input_field("Benutzernachname", "", 5, "color: blue;", self.on_name_aendert)
        self.defaultPassword_input = self.create_input_field("Benutzerkennwort", self.defaultPassword, 6, "color: black;")
        self.userName_input = self.create_input_field("Benutzername", "", 7, "color: black;", self.on_name_aendert)
        self.email_input = self.create_input_field("E-Mail", "", 8, "color: black;")
        
        #gruppen
        self.var_groups_list = []
        try:
            checkbox_enabled = True
            self.groups = self.get_existierte_ad_gruppen()
        except:    
            checkbox_enabled = False
            self.groups = ["nicht gefunden"]
        
        for i, group in enumerate(self.groups):
            checkbox = QtWidgets.QCheckBox(group, self)
            checkbox.setEnabled(checkbox_enabled)
            self.form_layout.addWidget(checkbox, 9 + i, 0, 1, 4)
            self.var_groups_list.append(checkbox)
        
        layout.addWidget(self.scroll_area)
        
        self.standardwertenEinstellen()

    def get_existierte_ad_gruppen(self):
        result = self.ps_run(f"Get-ADGroup -Filter * -SearchBase '{self.groupOU}' | Select-Object -ExpandProperty Name")
        groups = result.split('\n')
        return [group for group in groups if group and group.strip()]
        
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

        if len(self.vorname_input.text()) + len(self.nachname_input.text()) == 0:
            userName = ""
            emailAddress = ""

        self.userName_input.setText(userName)
        self.email_input.setText(emailAddress)
        self.pruefe_daten()
    
    def pruefe_daten(self):
        if len(self.userName_input.text()) == 0 or len(self.userName_input.text()) > 20:
            self.button_generiere.setEnabled(False)
            self.button_generiere.setStyleSheet("background-color: blue; color: gray;")
        else:    
            self.button_generiere.setEnabled(True)
            self.button_generiere.setStyleSheet("background-color: blue; color: white;")

    
    def on_generiere_button_click(self):
        selected_groups = [group.text() for i, group in enumerate(self.var_groups_list) if group.isChecked()]
        print(selected_groups)

        ps_new_aduser = f"""
            New-ADUser -GivenName '{self.vorname_input.text()}' `
            -Surname '{self.nachname_input.text()}' `
            -Name '{self.vorname_input.text()} {self.nachname_input.text()}' `
            -SamAccountName '{self.userName_input.text()}' `
            -UserPrincipalName '{self.email_input.text()}' `
            -EmailAddress '{self.email_input.text()}' `
            -Path '{self.userOU_input.text()}' `
            -AccountPassword (ConvertTo-SecureString '{self.defaultPassword_input.text()}' -AsPlainText -Force) `
            -PasswordNeverExpires $false `
            -ChangePasswordAtLogon $true `
            -Enabled $true
            """
        result = self.ps_run(ps_new_aduser)
        print(result)
        
        for group in selected_groups: 
            ps_user_group = f"Add-ADGroupMember -Identity {group} -Members {self.userName_input.text()}"
            result = self.ps_run(ps_user_group)
            print(result)

        self.standardwertenEinstellen()
    
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
        self.vorname_input.setFocus()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UserGenerator()
    window.setWindowTitle("Benutzergenerator")
    window.resize(800, 600)
    window.show()
    window.pruefe_daten()
    sys.exit(app.exec_())
