import requests

TENANT_ID = "1a4b030f-7004-48e0-a590-e19c2334409a"
TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJWS283NFdQQkZsU25sZ3FGSUJFS1pZUjAtbUNtaXB1V2pILVM2UmJFemRRIn0.eyJleHAiOjE3ODU1MTIyOTcsImlhdCI6MTc4NTQ5MDY5NywiYXV0aF90aW1lIjoxNzg1NDkwNjk0LCJqdGkiOiJlOGU5YjZhZS0xYzVmLTQzZTQtOGY0Zi1iMjY3MjFjMjI2NTAiLCJpc3MiOiJodHRwczovL2F1dGhlbnRpY2F0ZS5vcy53cHAuY29tL2F1dGgvcmVhbG1zL29zLXByb2QiLCJhdWQiOiJhY2NvdW50Iiwic3ViIjoiMmM1MzRiYTYtZjYxZC00ZjJmLWJiYTEtZjVlMjU5MzZiNmJkIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoib3Mtd2ViIiwic2Vzc2lvbl9zdGF0ZSI6IjM0ZGMzMjNkLTkwODItNDc1MC1iY2Q1LWVmNTVmZmEyZWY3NyIsInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtb3MtcHJvZCIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgZW1haWwgcHJvZmlsZSIsInNpZCI6IjM0ZGMzMjNkLTkwODItNDc1MC1iY2Q1LWVmNTVmZmEyZWY3NyIsInppcENvZGUiOiI2MDAwMDIiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImhvbWVPcmciOiJzc293MDEwIiwibWFuYWdlciI6ImhhcnNoZGVlcC5raG9sYUBjaG9yZW9ncmFwaC5jb20iLCJjaXR5IjoiQ2hlbm5haSIsImdlb1JlZ2lvbiI6IkFQQUMiLCJjdHgiOlsid29ya3NwYWNlX2lkOjRjMDM5MjE3LTdkMTctNDIwNy04MzE0LTk4MzQ4OTgzNzE4YSJdLCJva3RhSUQiOiIwMHVwMHVkcGF0bzVoTm9RczQxNyIsIkxvY2F0aW9uSUQiOiJBUEFDLUlOLUNIRU5OQUktMTQ4NiIsInByZWZlcnJlZF91c2VybmFtZSI6ImF6YXRoLmFAY2hvcmVvZ3JhcGguY29tIiwiZ2l2ZW5fbmFtZSI6IkF6YXRoIiwidGl0bGUiOiJPTVMgSW1wbGVtZW50YXRpb24gQW5hbHlzdCIsImV4dGVybmFsVXNlciI6ZmFsc2UsInRlbXBFbWFpbElEIjoiYXphdGguYUBjaG9yZW9ncmFwaC5jb20iLCJjb3VudHJ5Q29kZSI6IklOIiwibmFtZSI6IkF6YXRoIEEiLCJjbGllbnQiOiJ3cHAtb3BlbiIsImNvbXBhbnkiOiJDaG9yZW9ncmFwaCIsInN0YXRlIjoiVGFtaWxuYWR1IiwiZGVwYXJ0bWVudCI6IlByb2R1Y3QgU3VwcG9ydCIsImZhbWlseV9uYW1lIjoiQSIsImVtYWlsIjoiYXphdGguYUBjaG9yZW9ncmFwaC5jb20ifQ.ibWeOkKT_fGi4IU5mh7-ta9CMFk-MVPQP9ayBl2P0BGvKjvi748CePFt5xChL--22dhSG4IpbxM1Dkq1octheXF0dY1kk-PGskBLgsTBwEPpx9CM7Aq6P76g2ovvyzG7fFbFEVauj6MPpYvg83LPIYXQM5jc1OYanTGilGV7HqqQcn7k0rYfkIqEbw9b2Hy9HX0qQsSctTov0knEHt4Hyrb0j5Plp1ElSIWTzGRPGAVmAxxFtcfkGRvDhzE1_6_IbMlqntgj0XCtDVIZFaMo52HBBE-ObZy-G5oUGB0QG8CHaiFB-8zmYlGzt-iMN93nhnzJuOkuWaE93d9soMeo0w"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

# ------------------------------------------------------------------
# 1. Get roles for a member (email in path)
# ------------------------------------------------------------------

email = "harshdeep.khola@choreograph.com"

url = f"https://media.os.wpp.com/api/tenants/{TENANT_ID}/members/{email}/roles?page=1&itemsPerPage=50"

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)


# ------------------------------------------------------------------
# 2. Get roles filtered by user_id
# ------------------------------------------------------------------

user_id = "2f3660d3-dea6-4bee-895f-1b30905185ad"

url = f"https://media.os.wpp.com/api/tenants/{TENANT_ID}/roles"

params = {
    "page": 1,
    "itemsPerPage": 50,
    "filter[user_id]": user_id
}

response = requests.get(url, headers=headers, params=params)

print(response.status_code)
print(response.text)