from os import environ as env, path

if path.isfile('./.env'):
    from loadenv import load_env_file
    load_env_file()

def supabase_params(request):
    supabase_id = env.get('SUPABASE_URL').split('//')[1].split('.')[0]
    supabase_bucket_name = env.get('SUPABASE_IMAGES_BUCKET_NAME')
    return {
        "SUPABASE_ID": supabase_id,
        "SUPABASE_BUCKET_NAME": supabase_bucket_name }
