import ldap3
from ldap3 import Server, Connection, ALL

# Konfigurationsparameter (bitte anpassen)
AD_SERVER = 'ldap://your-ad-server.com'  # AD-Server-Adresse
AD_USER = 'your_username@domain.com'     # Benutzername mit Berechtigung zum Abfragen von AD
AD_PASSWORD = 'your_password'            # Passwort des Benutzers
BASE_DN = 'dc=domain,dc=com'             # Basis-DN der Domäne


def get_ad_groups(connection):
    """
    Verwendet eine bestehende Verbindung zu Active Directory und ruft alle Gruppen ab.
    
    Args:
        connection (ldap3.Connection): Eine aktive Verbindung zu Active Directory.
    
    Returns:
        list: Eine Liste mit den Namen der Gruppen in Active Directory.
    """
    try:
        # LDAP-Suchfilter, um alle Gruppen abzurufen
        search_filter = '(objectClass=group)'
        
        # Attribut, das wir abrufen möchten (cn = common name)
        attributes = ['cn']
        
        # Suche im Active Directory starten
        connection.search(search_base=BASE_DN, 
                          search_filter=search_filter, 
                          attributes=attributes)
        
        # Extrahiere die Gruppennamen aus den Suchergebnissen
        groups = [entry['attributes']['cn'] for entry in connection.entries]
        
        print(f"{len(groups)} Gruppen gefunden.")
        
        return groups
    
    except Exception as e:
        print(f"Fehler bei der Verbindung zu Active Directory: {e}")
        return []


def connect_to_ad():
    """
    Stellt eine Verbindung zu Active Directory her.
    
    Returns:
        ldap3.Connection: Eine aktive Verbindung zu Active Directory.
    """
    try:
        server = Server(AD_SERVER, get_info=ALL)
        connection = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)
        print("Verbindung zu Active Directory hergestellt.")
        return connection
    except Exception as e:
        print(f"Fehler bei der Verbindung zu Active Directory: {e}")
        return None


if __name__ == "__main__":
    connection = connect_to_ad()
    if connection:
        ad_groups = get_ad_groups(connection)
        connection.unbind()
        if ad_groups:
            print("Gefundene Gruppen:")
            for idx, group in enumerate(ad_groups, start=1):
                print(f"{idx}. {group}")
        else:
            print("Keine Gruppen gefunden oder Fehler bei der Verbindung zu AD.")
    else:
        print("Konnte keine Verbindung zu Active Directory herstellen.")
        