import paramiko
import os

def ssh_transfer(source_ip, source_username, source_password, dest_ip, dest_username, dest_password, source_folder,destination_folder):
    # Connect to Server 1
    source_client = paramiko.SSHClient()
    source_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    source_client.connect(source_ip, username=source_username, password=source_password)

    # Compress the folder on Server 1
    command = f"zip -r {source_folder}.zip {source_folder}"
    # stdin, stdout, stderr = source_client.exec_command(command)
    # source_client.close()
    print(source_client)

    # Connect to Server 2
    dest_client = paramiko.SSHClient()
    dest_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    dest_client.connect(dest_ip, username=dest_username, password=dest_password)

    # Transfer the zip file from Server 1 to Server 2
    sftp = dest_client.open_sftp()
    print(source_folder)
    sftp.put(f"{source_folder}.zip", f"{destination_folder}.zip")
    sftp.close()

    # Unzip the file on Server 2
    command = f"unzip -o {source_folder}.zip -d {source_folder}"
    stdin, stdout, stderr = dest_client.exec_command(command)
    dest_client.close()


# Example usage
source_ip = "62.67.51.161"
source_username = "root"
source_password = "6V69C5Qo70va0qdAK40z"
source_folder = "/media/HDD2/SmartlyFit/Data/production_data/UTRLC-1"
dest_ip = "62.67.203.8"
dest_username = "root"
dest_password = "QLwWKyQ3HHq$I!mEg"
destination_folder = "/home/workstation/StableVITON_train/Training_data/UTRLC-1"

ssh_transfer(source_ip, source_username, source_password, dest_ip, dest_username, dest_password, source_folder,destination_folder)
