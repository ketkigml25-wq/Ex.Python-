resources = {
  "R101": {"type":"Room", "status":"Free"},
  "D12": {"type":"Doctor", "status":"Available"}
}

resource_id = input("Enter resource ID: ")

if resource_id in resources:
  status = resources[resource_id]["status"]
  if status in ["Free", "Available"]:
    resources[resource_id]["status"] = "Allocated"
    print("Resource allocated")
  else:
    print("Resource unavailable")
else:
  print("Resource not found")
