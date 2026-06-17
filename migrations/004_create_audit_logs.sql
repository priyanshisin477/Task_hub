create table audit_logs (
  id uuid primary key default gen_random_uuid(),
  task_id uuid references task(id) on delete cascade,
  user_id uuid references users(id),
  action_text text not null,
  old_status text,
  new_status text,
  created_at timestamp with time zone default now()
);