import requests
import json
import getpass

JIRA_URL = "https://ayilasushmithareddy.atlassian.net"
print(f"Connecting to Jira: {JIRA_URL}")
email = input("Enter your Jira email address (e.g. ayila...): ").strip()
api_token = getpass.getpass("Enter your Jira API Token (or password): ").strip()

auth = (email, api_token)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# Test connection
res = requests.get(f"{JIRA_URL}/rest/api/3/myself", auth=auth, headers=headers)
if res.status_code != 200:
    print(f"Failed to authenticate with Jira: {res.status_code} {res.text}")
    exit(1)

print(f"Successfully authenticated as {res.json().get('displayName')}!")
print("Creating project AWMS...")

# Create AWMS Project via REST API
project_payload = {
    "key": "AWMS",
    "name": "Autonomous Warehouse Management System",
    "projectTypeKey": "software",
    "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-scrum-template",
    "leadAccountId": res.json().get("accountId")
}
proj_res = requests.post(f"{JIRA_URL}/rest/api/3/project", auth=auth, headers=headers, data=json.dumps(project_payload))
if proj_res.status_code in [200, 201]:
    print("Project AWMS created successfully!")
else:
    print(f"Project creation status: {proj_res.status_code} (Project may already exist)")

print("Import complete!")
