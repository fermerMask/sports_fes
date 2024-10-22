from supabase import create_client,Client

url: str = "https://vxmvhaazvkzvezovyvui.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ4bXZoYWF6dmt6dmV6b3Z5dnVpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc4NDYyMTcsImV4cCI6MjA0MzQyMjIxN30.L_xHRbQFYY60tmbpXqS9KzFFxlESp2_sZk-PGkeSuVo"

supabase: Client = create_client(url, key)

def find_all_date():
    data = supabase.table("user").select("*").execute()
    return data

result = find_all_date()

print(result)