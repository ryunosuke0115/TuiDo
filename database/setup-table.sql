CREATE TABLE public.task_table (
  id BIGINT primary key generated always as identity,
  name text,
  created_at timestamptz default now(),
  due_date timestamptz default null,
  is_completed boolean default false,
  description text default null
);

ALTER TABLE public.task_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all" ON public.task_table
FOR ALL
USING (true)
WITH CHECK (true);

CREATE TABLE public.tag_table (
  id BIGINT primary key generated always as identity,
  name text,
  description text default null
);

ALTER TABLE public.tag_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all" ON public.tag_table
FOR ALL
USING (true)
WITH CHECK (true);

CREATE TABLE public.task_tag_join_table (
  task_id BIGINT NOT NULL REFERENCES public.task_table(id) ON DELETE CASCADE,
  tag_id BIGINT NOT NULL REFERENCES public.tag_table(id) ON DELETE CASCADE,
  PRIMARY KEY (task_id, tag_id)
);

ALTER TABLE public.task_tag_join_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all" ON public.task_tag_join_table
FOR ALL
USING (true)
WITH CHECK (true);

CREATE VIEW public.task_tag_view AS
SELECT
  ts.id AS task_id,
  ts.name AS task_name,
  ts.created_at AS task_created_at,
  ts.due_date AS task_due_date,
  ts.is_completed AS task_is_completed,
  ts.description AS task_description,
  tg.id AS tag_id,
  tg.name AS tag_name,
  tg.description AS tag_description
FROM task_table AS ts
JOIN task_tag_join_table AS tt
  ON ts.id = tt.task_id
JOIN tag_table AS tg
  ON tt.tag_id = tg.id;
