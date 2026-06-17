create table generated_image (
  id uuid primary key default gen_random_uuid(),
  task_id uuid references task(id) on delete cascade,
  
  image_type text not null,
  image_url text,
  prompt_used text,
  angle text,
  metadata jsonb,
  created_at timestamp with time zone default now()
);