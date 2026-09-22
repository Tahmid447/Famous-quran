-- Apply only to the owner's approved Supabase project.
create table if not exists public.fq_backups (
 user_id uuid primary key references auth.users(id) on delete cascade,
 payload jsonb not null check (octet_length(payload::text) < 5242880),
 updated_at timestamptz not null default now()
);
alter table public.fq_backups enable row level security;
revoke all on public.fq_backups from anon;
grant select, insert, update, delete on public.fq_backups to authenticated;
create policy "read own backup" on public.fq_backups for select to authenticated using ((select auth.uid()) = user_id);
create policy "insert own backup" on public.fq_backups for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "update own backup" on public.fq_backups for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "delete own backup" on public.fq_backups for delete to authenticated using ((select auth.uid()) = user_id);
