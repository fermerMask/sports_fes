from supabase import create_client,Client

supabase: Client = create_client(url, key)

def find_all_date():
    data = supabase.table("user").select("*").execute()
    return data

result = find_all_date()

print(result)