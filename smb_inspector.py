#from impacket.smbconnection import SMBConnection
from smb.SMBConnection import SMBConnection
from smb.security_descriptors import ACE_TYPE_ACCESS_ALLOWED, ACE_TYPE_ACCESS_DENIED, SID_CREATOR_OWNER, SID_CREATOR_GROUP
from impacket import smb
import argparse
import os
from nmb.NetBIOS import NetBIOS
import array
import re

# Defining Colours
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'  # Reset color

# Dictionary of Permissions
permis_dict = {
    "80000000": "Generic Read",
    "40000000": "Generic Write",
    "20000000": "Generic Execute",
    "10000000": "Generic All",

    "00080000": "Write Owner",
    "00040000": "Write DAC",
    "0020000": "Read Control",
    "00010000": "Delete",

    "1F01FF": "File All Access",
    "1200A0": "File Execute",
    "120116": "File Write",
    "120089": "File Read",

    "000F003F": "Key All Access",
    "00020019": "Key Read",
    "00020019": "Key Execute",
    "00020006": "Key Write",

    "00000100": "Control Access",
    "00000080": "List Object",
    "00000040": "Delete Tree",
    "00000020": "Write Property",
    "00000010": "Read Property",
    "00000008": "Self Write",
    "00000004": "List Children",
    "00000002": "Delete Child",
    "00000001": "Create Child",
}

sids_dict = {
    "S-1-1-0": "Everyone",
    "S-1-0-0": "NULL",
    "S-1-5-7": "Anonymous",
    "S-1-5-11": "Authenticated Users",
}

files_dict = {

}

# Shares that are pulled from listShares()
found_shares = []
found_directories = []
dangerous_files = []
found_files = []
path_root = "/"
hosts = []

def read_target(target):
    with open(target, "r") as target:
        for line in target:
            hosts.append(line.strip("\n''"))

# Function to connect to share and path
def share_connect(connection, share, path=None):
    files = connection.listPath(share, path)
    return files

def file_permissions(connection, share, path=None):
    info = connection.getSecurity(share, path)
    return info

def search_dangerous_perms(file, path, full_path):
    global dangerous_files
    for perm in file.dacl.aces:
        if str(perm.sid) in sids_dict.keys():
            access = hex(perm.mask)[2:].upper()
            if access in permis_dict.keys():
                files_dict[full_path] = access
        else:
            pass

def list_dangerous():
    print (f"\n{BLUE}Scan Complete. Dumping dangerous files...  {END}")
    print (f"--------------------------------")
    for k,v in files_dict.items():
        print (f'{RED}File {k}, Permission: {permis_dict[v]}{END}')

def list_interesting():
    global found_files
    print (f"\n{BLUE}Scan Complete. Dumping interesting files...  {END}")
    print (f"--------------------------------")
    for file in found_files:
        print(f'{GREEN}{file}{END}')

def recursive_search(connection, share, dir):
    sub_dir = []
    global found_files
    files = share_connect(connection, share.name, dir)
    print (f"\n{YELLOW}Listing {share.name}{dir}... {END}")
    print (f"--------------------------------")
    for f in files:
        full_path = share.name + os.path.join(dir,f.filename)
        search_interesting_extensions(full_path)
        if f.filename not in (".", ".."):
            if f.isDirectory:
                file_sec = connection.getSecurity(f"{share.name}", f"{dir}/{f.filename}")
                search_dangerous_perms(file_sec, f.filename, full_path)
                sub_dir.append(os.path.join(dir,f.filename))
                print (f"Directory - {f.filename}")
            else:
                file_sec = connection.getSecurity(f"{share.name}", f"{dir}/{f.filename}")
                search_dangerous_perms(file_sec, f.filename, full_path)
                print (f"File - {dir}/{f.filename}")
    for sub in sub_dir:            
        recursive_search(connection, share, sub)

def search_interesting_extensions(file):
    dangerous_file_extensions = ['.ps1', '.bat', '.cmd', '.sh', '.vbs', '.js', '.jar', '.py', '.com', '.pif', '.vb', '.scr', '.ws', '.wsh', '.msc',  '.reg', '.jar', '.app', '.ade', '.adp', '.lnk']
    sensitive_file_extensions = ['.doc', '.docx', '.xls', '.xlsx', '.pdf', '.txt', '.csv', '.log', '.xml', '.json', '.sql', '.config', '.ini', '.env', '.key', '.pem', '.cer', '.pfx', '.p12', '.private', '.pub', '.ssh', '.backup', '.bak', '.db', '.mdb', '.sqlite', '.dbf', '.csv']
    all_dangerous_extensions = dangerous_file_extensions + sensitive_file_extensions
    extension = '.' + file.split('.')[-1].lower()
    if extension in all_dangerous_extensions:
        found_files.append(file)

class share_info:
    _share_classes = []

    def __init__(self, name, dir=None, files=None):
        self.name = name
        self.dirs = []
        self.files = [files]
        self.interesting_files = []
        self._share_classes.append(self)

# List shares found on the remote host
def list_shares(connection):
    global found_shares
    share_ = "Share_" 
    try:
        shares = connection.listShares()
        print(f"\nFound Shares:")
        print(f"==========================================\n")
        for share in shares:
            name = share.name
            if share.name in ('ADMIN$', 'C$', 'IPC$'):
                pass
                print(f"[DEBUG] skipping {name}")
            else:
                print(f"{GREEN}Found share Name: {name} {END}")
                class_creation = share_ + name
                class_creation = share_info(name)

            print("------")
    except Exception as e:
        print(f"Failed to list shares\nReason: {str(e)}")
    
# List files found on shares.
def list_files(connection, share):
    global path_root
    global found_files
    class_instance = share
    try:
        files = share_connect(connection, share.name, path_root)
        for f in files:
            if f.filename not in (".", ".."):
                if f.isDirectory:
                    class_instance.dirs.append(path_root + f.filename)
                else:
                    print (f"\n{YELLOW}Listing {share.name}... {END}")
                    print (f"--------------------------------")
                    print (f"File - {f.filename}")

        if class_instance.dirs == "":
            pass
        else:
            for p in class_instance.dirs:
                sub_dir = []
                share.name 
                path = os.path.join(share.name, p)
                files = share_connect(connection, share.name, p)
                print (f"\n{YELLOW}Listing {share.name}{path}... {END}")
                print (f"--------------------------------")
                for f in files:
                    full_path = share.name + os.path.join(path,f.filename)
                    if f.filename not in (".", ".."):
                        search_interesting_extensions(full_path)
                        if f.isDirectory:
                            file_sec = connection.getSecurity(f"{share.name}", f"{path}/{f.filename}")
                            search_dangerous_perms(file_sec, f.filename, full_path)
                            sub_dir.append(os.path.join(p,f.filename))
                            print (f"Directory - {f.filename}")
                        else:
                            file_sec = connection.getSecurity(f"{share.name}", f"{path}/{f.filename}")
                            search_dangerous_perms(file_sec, f.filename, full_path)
                            print (f"File - {p}/{f.filename}")
            for sub in sub_dir:
                recursive_search(connection, share, sub)

    except smb.SessionError as e:
        print(f"SMB SessionError: {e.getErrorCode()}")
        print(f"Error message: {e.getErrorString()}")
        print(f"Error packet: {e.getErrorPacket()}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="SMB Recursive File List Script")
    parser.add_argument('-i', '--ip', dest='ip', required=False, default=None, help="Target SMB server IP address.")
    parser.add_argument('-t', '--target-file', dest='target', required=False, default=None, help="Target file for scanning multiple hosts.")
    parser.add_argument('-u', '--username', dest='username', required=True, help="Target SMB username.")
    parser.add_argument('-p', '--password', dest='password', required=True, help="Target SMB user password.")
    parser.add_argument('-v', '--verbose', dest='verbose', required=False, default=False, action=argparse.BooleanOptionalAction, help='This option will enable the program to be more or less verbose.')
    parser.add_argument('-s', '--share', dest='share', required=False, default=False, help='SMB share name')

    args = parser.parse_args()

    if args.verbose:
        print("[DEBUG] Username: " + args.username)
        print("[DEBUG] Password: " + args.password)
        # print("[DEBUG] IP Address: " + args.ip)

    con = None # Reset connection

    if args.ip is None and args.target is None:
        print ("Either an IP or target file must be provided! See help for more information")
    elif args.ip is not None and args.target is not None:
        print ("Either an IP or target file must be provided! You cannot use both simulatiously! See help for more information")
    elif args.ip is not None:
        try:
            con = SMBConnection(args.username, args.password, 'Client', args.ip, is_direct_tcp=True)
            con.connect(args.ip, 445)
            netbios = NetBIOS()
            server_name = netbios.queryIPForName(args.ip, timeout=5000)  # Timeout is in milliseconds
            print(f"Connected to - {YELLOW}{str(server_name).strip('[]''')}{END}")
            list_shares(con)
            for share_instance in share_info._share_classes:
                print(f"\n{YELLOW}Connecting to {share_instance.name} {END}")
                print(f"\n{YELLOW}==========================================={END}")
                list_files(con, share_instance)    
            list_dangerous()
            list_interesting()

        except Exception as e:
            print("Failed to connect or list files\nReason: " + str(e))


    elif args.target is not None:
        global hosts
        try:
            read_target(args.target)
            for host in hosts:
                if re.compile(r'^(\d{1,3}\.){3}\d{1,3}$').match(host):
                    con = SMBConnection(args.username, args.password, 'Client', host, is_direct_tcp=True)
                    con.connect(host, 445)
                    netbios = NetBIOS()
                    server_name = netbios.queryIPForName(host, timeout=5000)  # Timeout is in milliseconds
                    print(f"Connected to - {YELLOW}{str(server_name).strip('[]''')}{END}")
                    list_shares(con)
                    for share_instance in share_info._share_classes:
                        print(f"\n{YELLOW}Connecting to {share_instance.name} {END}")
                        print(f"\n{YELLOW}==========================================={END}")
                        list_files(con, share_instance)    
                    list_dangerous()
                    list_interesting()
                else:
                    print(f"\n{YELLOW}{host} is not a valid IP address... SKIPPING! {END}")

        except Exception as e:
            print("Failed to connect or list files\nReason: " + str(e))

if __name__ == "__main__":
    main()
