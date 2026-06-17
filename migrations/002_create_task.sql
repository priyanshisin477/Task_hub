create table task (
  id uuid primary key default gen_random_uuid(),
  tittle text,
  description text,
  status text default 'pending',
  assigned_by uuid references users(id),
  product_img_url text,
  created_at timestamp with time zone default now()
);