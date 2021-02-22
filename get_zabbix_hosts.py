import csv
import sys
from pyzabbix.api import ZabbixAPI


url = input("Type Zabbix URL: ")
login = input("Type login: ")
password = input("Type password: ")

zapi = ZabbixAPI(url=url, user=login, password=password)

hosts = zapi.host.get(output=["hostid", "name", "status"])

print("Hosts in total:", len(hosts))

enriched_hosts = list()

for host in hosts:
    enriched_host = dict()
    enriched_host["name"] = host["name"]
    enriched_host["status"] = host["status"]
    host_id = host["hostid"]
    interfaces = [host_interface["ip"] for host_interface in zapi.hostinterface.get(hostids=host_id, output=["ip"])]
    enriched_host["interfaces"] = interfaces
    groups = [host_group["name"] for host_group in zapi.hostgroup.get(hostids=host_id, output=["name"])]
    enriched_host["groups"] = groups
    templates = [template["name"] for template in zapi.template.get(hostids=host_id, output=["name"])]
    enriched_host["templates"] = templates
    enriched_hosts.append(enriched_host)

print("All hosts were enriched")

with open("hosts.csv", "w", newline="") as csvfile:
    fieldnames = ["name", "status", "interfaces", "groups", "templates"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for enriched_host in enriched_hosts:
        writer.writerow({"name": enriched_host["name"], "status": enriched_host["status"],
                         "interfaces": enriched_host["interfaces"], "groups": enriched_host["groups"],
                         "templates": enriched_host["templates"]})

print("All hosts were written to the hosts.csv")

zapi.user.logout()
