
#!/usr/bin/env python
#
# WW: import-module ActiveDirectory
# WS: Add-WindowsFeature -Name "RSAT-AD-PowerShell" -IncludeAllSubFeature
#

import sys
import msvcrt
import subprocess
import configparser
from PyQt5 import QtWidgets
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

neuer_benutzer_prefix = "<neuer Benutzer>"

class UserGenerator(QtWidgets.QWidget):
    
    def __init__(self):
        super().__init__()

        try:
            config = configparser.ConfigParser()
            config.read('AD-NeuerBenutzer-Pyqt.cfg')
            self.defaultPassword = config['Config']['defaultPassword']
            self.userOU = config['Config']['userOU'] 
            self.groupOU = config['Config']['groupOU']
            self.domainName = config['Config']['domainName']

            self.init_ui()
        except:
            QtWidgets.QMessageBox.critical(self, 'Fehler', 'Ein Fehler beim Lesen der Config-Datei.')
        
    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scrollable_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scrollable_widget)
        self.form_layout = QtWidgets.QGridLayout(self.scrollable_widget)

        #buttons        
        self.button_generiere = QtWidgets.QPushButton("Ausführen", self)
        self.button_generiere.clicked.connect(self.on_generiere_button_click)
        self.form_layout.addWidget(self.button_generiere, 0, 1)
        
        self.button_standardwert = QtWidgets.QPushButton("Standardwert", self)
        self.button_standardwert.clicked.connect(self.on_default_button_click)
        self.form_layout.addWidget(self.button_standardwert, 0, 2)
        
        self.button_schliessen = QtWidgets.QPushButton("Schließen", self)
        self.button_schliessen.clicked.connect(self.close)
        self.form_layout.addWidget(self.button_schliessen, 0, 3)

        #daten read only
        self.userOU_input = self.create_input_field("Benutzer OU", self.userOU, 1, "color: gray;", "color: gray;")
        self.userOU_input.setReadOnly(True)
        self.groupOU_input = self.create_input_field("Gruppe OU", self.groupOU, 2, "color: gray;", "color: gray;")
        self.groupOU_input.setReadOnly(True)
        self.domainName_input = self.create_input_field("Domänename", self.domainName, 3, "color: gray;", "color: gray;")
        self.domainName_input.setReadOnly(True)

        #benutzer name & zustand
        #benutzername
        label = QtWidgets.QLabel("Benutzername", self)    
        label.setStyleSheet("color: black;")
        self.form_layout.addWidget(label, 4, 1)
        self.benutzername_combo = QtWidgets.QComboBox(self)
        self.benutzername_combo.activated.connect(self.on_benutzernamecombo_aendert)
        self.benutzer_hinzufuegen()
        self.form_layout.addWidget(self.benutzername_combo, 4, 2)
        #zustand
        self.zustand_checkbox = QtWidgets.QCheckBox('Deaktiviert', self)
        self.zustand_checkbox.setStyleSheet("color: red;")
        self.form_layout.addWidget(self.zustand_checkbox, 4, 3)

        #daten & validators
        #vorname
        name_regex = QRegExp("^[A-Za-z0-9\\- ]{1,50}$")
        self.vorname_input = self.create_input_field("Benutzer-vorname", "", 5, "color: blue;", "color: black;", self.on_vornachname_aendert)
        vorname_validator = QRegExpValidator(name_regex, self.vorname_input)
        self.vorname_input.setValidator(vorname_validator)
        #vor- nachname ändern
        self.vornachname_checkbox = QtWidgets.QCheckBox('Ändern', self)
        self.vornachname_checkbox.clicked.connect(self.on_vornachname_checkbox_clicked)
        self.vornachname_checkbox.setStyleSheet("color: red;")
        self.form_layout.addWidget(self.vornachname_checkbox, 5, 3)
        #nachname
        self.nachname_input = self.create_input_field("Benutzer-nachname", "", 6, "color: blue;", "color: black;", self.on_vornachname_aendert)
        nachname_validator = QRegExpValidator(name_regex, self.vorname_input)
        self.nachname_input.setValidator(nachname_validator)
        #passwort
        self.defaultPassword_input = self.create_input_field("Benutzerkennwort", self.defaultPassword, 7, "color: black;", "color: black;")
        passwort_regex = QRegExp("^[a-zA-Z0-9!@#$%^&*()_+.,;:<>?~=-]{8,30}$")
        passwort_validator = QRegExpValidator(passwort_regex, self.defaultPassword_input)
        self.defaultPassword_input.setValidator(passwort_validator)
        #passwort ändern
        self.passwort_checkbox = QtWidgets.QCheckBox('Ändern', self)
        self.passwort_checkbox.clicked.connect(self.on_pass_checkbox_clicked)
        self.passwort_checkbox.setStyleSheet("color: red;")
        self.form_layout.addWidget(self.passwort_checkbox, 7, 3)
        #benutzername
        self.userName_input = self.create_input_field("Benutzername", "", 8, "color: black;", "color: black;", self.on_benutzername_aendert)
        username_regex = QRegExp("^[a-zA-Z0-9_]{1,20}$")
        username_validator = QRegExpValidator(username_regex, self.userName_input)
        self.userName_input.setValidator(username_validator)
        #email
        self.email_input = self.create_input_field("E-Mail", "", 9, "color: black;", "color: black;")
        email_regex = QRegExp(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        email_validator = QRegExpValidator(email_regex, self.email_input)
        self.email_input.setValidator(email_validator)
        #email ändern
        self.email_checkbox = QtWidgets.QCheckBox('Ändern', self)
        self.email_checkbox.clicked.connect(self.on_email_checkbox_clicked)
        self.email_checkbox.setStyleSheet("color: red;")
        self.form_layout.addWidget(self.email_checkbox, 9, 3)
        
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
            self.form_layout.addWidget(checkbox, 10 + i, 0, 1, 4)
            self.var_groups_list.append(checkbox)

        #groups ändern
        self.groups_checkbox = QtWidgets.QCheckBox('Ändern', self)
        self.groups_checkbox.clicked.connect(self.on_groups_checkbox_clicked)
        self.groups_checkbox.setStyleSheet("color: red;")
        self.form_layout.addWidget(self.groups_checkbox, 10, 3)

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        layout.addWidget(self.scroll_area)
        self.standardwertenEinstellen()

    def benutzer_hinzufuegen(self):
        self.benutzername_combo.clear()
        self.benutzername_combo.addItem(neuer_benutzer_prefix)

        result = self.ps_run(f"Get-ADUser -Filter * -SearchBase '{self.userOU}' | Select-Object -ExpandProperty UserPrincipalname")
        self.users = result.split('\n')
        for i, user in enumerate(self.users):
            if user.strip() != "":
                self.benutzername_combo.addItem(user)
        
    def get_existierte_ad_gruppen(self):
        result = self.ps_run(f"Get-ADGroup -Filter * -SearchBase '{self.groupOU}' | Select-Object -ExpandProperty Name")
        groups = result.split('\n')
        return [group for group in groups if group and group.strip()]
        
    def create_input_field(self, label_text, default_value, row, LabelStyle, LineEditStyle, callback=None):
        label = QtWidgets.QLabel(label_text, self)
        label.setStyleSheet(LabelStyle)
        self.form_layout.addWidget(label, row, 1)
        input_field = QtWidgets.QLineEdit(self)
        input_field.setStyleSheet(LineEditStyle)
        input_field.setText(default_value)
        if callback:
            input_field.textChanged.connect(callback)
        self.form_layout.addWidget(input_field, row, 2)
        return input_field
        
    def on_vornachname_aendert(self):
        if self.benutzername_combo.currentText() == neuer_benutzer_prefix: 
            userName = f"{self.vorname_input.text().lower()}.{self.nachname_input.text().lower()}"
            emailAddress = f"{userName}@{self.domainName_input.text()}"

            if len(self.vorname_input.text()) + len(self.nachname_input.text()) == 0:
                userName = ""
                emailAddress = ""

            self.userName_input.setText(userName)
            self.email_input.setText(emailAddress)
    
        self.pruefe_daten()

    def on_benutzername_aendert(self):
        self.pruefe_daten()

    def on_benutzernamecombo_aendert(self):
        if self.benutzername_combo.currentText() == neuer_benutzer_prefix:
            self.passwort_checkbox.setChecked(True)
            self.vornachname_checkbox.setChecked(True)
            self.email_checkbox.setChecked(True)
            self.set_groups_checkbox_state(True)
            self.defaultPassword_input.setText(self.defaultPassword)
            self.vorname_input.setText("")
            self.nachname_input.setText("")
            self.email_input.setText("")
        else:
            self.passwort_checkbox.setChecked(False)
            self.vornachname_checkbox.setChecked(False)
            self.email_checkbox.setChecked(False)
            self.set_groups_checkbox_state(False)
            self.setEnabled(False)
            self.defaultPassword_input.setText("")
            self.vorname_input.setText("")
            self.nachname_input.setText("")
            self.email_input.setText("")

            self.progress_bar.setValue(11)
            result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" | Select-Object -ExpandProperty SamAccountName")
            samaccount_text = result.split('\n')

            self.progress_bar.setValue(22)
            result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" | Select-Object -ExpandProperty GivenName")
            vorname_text = result.split('\n')

            self.progress_bar.setValue(44)
            result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" | Select-Object -ExpandProperty Surname")
            nachname_text = result.split('\n')
            
            self.progress_bar.setValue(66)
            result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" -Properties * | Select-Object -ExpandProperty mail")
            email_text = result.split('\n')

            self.progress_bar.setValue(77)
            result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" | Select-Object -ExpandProperty Enabled")
            text = result.split('\n')
            if text[0] == "True":
                self.zustand_checkbox.setChecked(False)
            else:
                self.zustand_checkbox.setChecked(True)    

            self.progress_bar.setValue(99)
            result = self.ps_run(f"Get-ADPrincipalGroupMembership {samaccount_text[0]} | Select-Object -ExpandProperty Name")
            groups_text = result.split('\n')

            self.userName_input.setText(samaccount_text[0])
            self.vorname_input.setText(vorname_text[0])
            self.nachname_input.setText(nachname_text[0])
            self.email_input.setText(email_text[0])

            for i, group in enumerate(self.var_groups_list):
                group.setChecked(group.text() in groups_text)

            self.setEnabled(True)
            self.progress_bar.setValue(0)

        self.pruefe_daten()    

    def pruefe_daten(self):
        if len(self.userName_input.text()) == 0 or len(self.userName_input.text()) > 20:
            self.button_generiere.setEnabled(False)
            self.button_generiere.setStyleSheet("background-color: blue; color: gray;")
        else:    
            self.button_generiere.setEnabled(True)
            self.button_generiere.setStyleSheet("background-color: blue; color: white;")

        if self.benutzername_combo.currentText() == neuer_benutzer_prefix:
            self.userName_input.setEnabled(True)
        else:
            self.userName_input.setEnabled(False)

        self.defaultPassword_input.setEnabled(self.passwort_checkbox.isChecked())
        self.vorname_input.setEnabled(self.vornachname_checkbox.isChecked())
        self.nachname_input.setEnabled(self.vornachname_checkbox.isChecked())
        self.email_input.setEnabled(self.email_checkbox.isChecked())
        self.set_groups_checkbox_state(self.groups_checkbox.isChecked())

    def on_generiere_button_click(self):
        selected_groups = [group.text() for i, group in enumerate(self.var_groups_list) if group.isChecked()]

        self.setEnabled(False)

        if self.benutzername_combo.currentText() == neuer_benutzer_prefix: 
            #Benutzer anlegen
            try:
                self.progress_bar.setValue(44)
                ps_new_aduser = f""" `
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
        
                self.progress_bar.setValue(99)
                for group in selected_groups: 
                    ps_user_group = f"Add-ADGroupMember -Identity \"{group}\" -Members {self.userName_input.text()}"
                    result = self.ps_run(ps_user_group)

                QtWidgets.QMessageBox.information(self, 'Erfolg', 'Die Operation wurde erfolgreich beendet.')
                self.standardwertenEinstellen()
            except:
                QtWidgets.QMessageBox.critical(self, 'Fehler', 'Die Operation wurde nicht erfolgreich beendet.')
        else:
            #Zustand ändern
            try:
                self.progress_bar.setValue(11)
                result = self.ps_run(f"Get-ADUser -filter \"UserPrincipalName -eq '{self.benutzername_combo.currentText()}'\" | Select-Object -ExpandProperty SamAccountName")
                samaccount_text = result.split('\n')
                
                self.benutzer_zustand = '$false' if self.zustand_checkbox .isChecked() else '$true'
                self.progress_bar.setValue(22)
                result = self.ps_run(f"Set-ADUser {samaccount_text[0]} -Enabled {self.benutzer_zustand}")

                #Vor-Nachname ändern
                if self.vornachname_checkbox.isChecked():
                    self.progress_bar.setValue(99)
                    result = self.ps_run(f"Set-ADUser {samaccount_text[0]} -GivenName \"{self.vorname_input.text()}\" -Surname \"{self.nachname_input.text()}\"")

                #EMail ändern
                if self.email_checkbox.isChecked():
                    self.progress_bar.setValue(99)
                    result = self.ps_run(f"Set-ADUser {samaccount_text[0]} -EMailAddress \"{self.email_input.text()}\"")

                #Benutzerpass ändern
                if self.passwort_checkbox.isChecked():
                    self.progress_bar.setValue(99)
                    result = self.ps_run(f"Set-ADAccountPassword {samaccount_text[0]} -Reset -NewPassword (ConvertTo-SecureString '{self.defaultPassword_input.text()}' -AsPlainText -Force)")

                #groups andern
                if self.groups_checkbox.isChecked():
                    self.progress_bar.setValue(99)
                    for i, group in enumerate(self.var_groups_list):
                        if group.isChecked():
                            ps_user_group = f"Add-ADGroupMember -Identity \"{group.text()}\" -Members {self.userName_input.text()} -Confirm:$false"
                        else:
                            ps_user_group = f"Remove-ADGroupMember -Identity \"{group.text()}\" -Members {self.userName_input.text()} -Confirm:$false"

                QtWidgets.QMessageBox.information(self, 'Erfolg', 'Die Operation wurde erfolgreich beendet.')
                self.standardwertenEinstellen()
            except:
                QtWidgets.QMessageBox.critical(self, 'Fehler', 'Die Operation wurde nicht erfolgreich beendet.')

        self.setEnabled(True)
        self.progress_bar.setValue(00)
    
    def on_default_button_click(self):
        self.standardwertenEinstellen()

    def on_pass_checkbox_clicked(self):
        self.defaultPassword_input.setEnabled(self.passwort_checkbox.isChecked())

    def on_vornachname_checkbox_clicked(self):        
        self.vorname_input.setEnabled(self.vornachname_checkbox.isChecked())
        self.nachname_input.setEnabled(self.vornachname_checkbox.isChecked())

    def on_email_checkbox_clicked(self):    
        self.email_input.setEnabled(self.email_checkbox.isChecked())

    def on_groups_checkbox_clicked(self):
        self.set_groups_checkbox_state(self.groups_checkbox.isChecked())

    def set_groups_checkbox_state(self, state):
        for i, group in enumerate(self.var_groups_list):
            group.setEnabled(state)

    def ps_run(self, ps_command):
        completed = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True, check=True)
        return completed.stdout

    def standardwertenEinstellen(self):
        self.setEnabled(False)
        self.progress_bar.setValue(22)

        self.userOU_input.setText(self.userOU)
        self.groupOU_input.setText(self.groupOU)
        self.domainName_input.setText(self.domainName)
        self.vorname_input.setText("")
        self.nachname_input.setText("")
        self.defaultPassword_input.setText(self.defaultPassword)
        self.userName_input.setText("")
        self.email_input.setText("")
        
        self.defaultPassword_input.setEnabled(True)
        self.passwort_checkbox.setChecked(True)
        self.vornachname_checkbox.setChecked(True)
        self.email_checkbox.setChecked(True)

        self.progress_bar.setValue(99)
        self.benutzer_hinzufuegen()

        for i, group in enumerate(self.var_groups_list):
            group.setChecked(False)
        self.set_groups_checkbox_state(True)

        self.progress_bar.setValue(0)
        self.setEnabled(True)
        self.pruefe_daten()
        self.vorname_input.setFocus()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('.QLabel { font-size: 10pt;} .QComboBox { font-size: 10pt;} .QCheckBox { font-size: 10pt;} .QLineEdit { font-size: 10pt;} .QPushButton { font-size: 10pt;}')

    window = UserGenerator()
    window.setWindowTitle("AD Benutzer anlegen/anpassen")
    window.resize(900, 600)
    window.show()
    window.pruefe_daten()

    sys.exit(app.exec_())
