create table users (
    id uuid primary key default gen_random_uuid(),
    emai text unique not null,
    name text,
    role text default 'user',
    avatar_url text,
    created_at timestamp with time zone now()

)