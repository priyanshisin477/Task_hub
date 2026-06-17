create policy "users_select_own_tasks"
on tasks for select 
using (
  assigned_by = auth.uid()
  or created_by = auth.uid()
);

create policy "admin_select_all_tasks"
on tasks for select
using (
  exists (
    select 1 from users
    where id = auth.uid()
    and role = 'admin'
  )
);

-- User can only see their own generated images
create policy "users_select_own_images"
on generated_image for select
using (
  exists (
    select 1 from tasks
    where tasks.id = generated_image.task_id
    and tasks.assigned_by = auth.uid()
  )
);

-- Admin can see all generated images
create policy "admin_select_all_images"
on generated_image for select
using (
  exists (
    select 1 from users
    where id = auth.uid()
    and role = 'admin'
  )
);

-- Only admin can see audit logs
create policy "admin_select_all_logs"
on audit_logs for select
using (
  exists (
    select 1 from users
    where id = auth.uid()
    and role = 'admin'
  )
);