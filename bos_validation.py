## Required modules
import os
import subprocess
import re
import pyodbc
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

## Environment variables 
SUBSCRIPTION = os.getenv('SUBSCRIPTION')
RESOURCE_GROUP = os.getenv('RESOURCE_GROUP')
VNET_NAME = os.getenv('VNET_NAME')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')

## PowerShell command variables ##
json_path = r'C:\Agent03\output\vnet-data-complete.txt'
ps_path = r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'
encoding_format = r"ascii"

# ## Login command

# login = f"""
# $username = "{USER_NAME}"
# $password = ConvertTo-SecureString {PASSWORD} -AsPlainText -Force
# $cred = new-object system.management.automation.PSCredential $username,$Password

# Connect-AzAccount -Credential $Cred -Tenant '***************' -ServicePrincipal"""

# subprocess.run([ps_path, login])

## Command to extract data as JSON from the subnet of the virtual machine scale-set
ps_cmd = f"""Set-AzContext -Subscription {SUBSCRIPTION}
$result=Get-AzVirtualNetwork -Name {VNET_NAME}  -ResourceGroupName {RESOURCE_GROUP} -ExpandResource 'subnets/ipConfigurations'
$result.Subnets[0].IpConfigurations | Out-File -FilePath {json_path} -Encoding {encoding_format}"""

## Exceute powershell command
subprocess.run([ps_path, ps_cmd])

# Extract all the Private IPs from the output file
with open(r"C:\Agent03\output\vnet-data-complete.txt") as fh:
  output = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', fh.read())


first_ip = output[0]

# SQL Connection credentials

conn = pyodbc.connect(DRIVER='{SQL Server}',
                       SERVER='******',
                       DATABASE='*****',
                       UID='*******',
                       PWD='*******')

## Query operational DB and extract all the active workers and their IP addresses.

vmss_data = pd.read_sql_query(''' 
                             SELECT TOP (100) 
                            [SdrVersion]
                            ,[IPAddress]
                            FROM [dbo].[Worker]
                              '''
                              ,conn) 


## Get SDR version 

print (vmss_data)

sdr = open(r"C:\Agent03\output\sdrversion.txt","r",encoding="utf-8")
sdr_version = sdr.read().rstrip('\n')

# ## Check the latest SDR version in BOS workers
# if sdr_version in vmss_data.values:
#   print (f"BOS has been updraded successfully to version {sdr_version}")
# else:
#   print ("BOS deployment was failed")

# ## Check if IP has been reimaged succesfully

if (first_ip in vmss_data.values and sdr_version in vmss_data.values):
  print (f"BOS has been updraded successfully to version {sdr_version}")
else:
  raise ValueError (f"BOS deployment was failed!")


## Need to count instances and compare to the running
