-- SkipperQuiz course API schema. Applied idempotently on boot (db.init).

create table if not exists purchases (
  id           serial primary key,
  email        text not null,
  amount_ils   numeric(10,2),
  coupon_code  text,
  partner_ref  text,               -- influencer/partner attribution
  tranzila_txn text unique,        -- Tranzila transaction id, dedupes double-notify
  status       text not null default 'paid',
  created_at   timestamptz not null default now()
);

create table if not exists access_codes (
  code         text primary key,
  email        text not null,
  purchase_id  int references purchases(id),
  device_limit int not null default 2,
  revoked      boolean not null default false,
  created_at   timestamptz not null default now()
);
create index if not exists idx_access_codes_email on access_codes(email);

-- checkout order token (links a pending checkout to its notify callback)
alter table purchases add column if not exists token text;
create unique index if not exists idx_purchases_token on purchases(token);

create table if not exists code_devices (
  code       text not null references access_codes(code) on delete cascade,
  device_id  text not null,
  first_seen timestamptz not null default now(),
  last_seen  timestamptz not null default now(),
  primary key (code, device_id)
);

create table if not exists progress (
  code       text primary key references access_codes(code) on delete cascade,
  data       jsonb not null default '{}'::jsonb,   -- XP, SRS, topicStats, done
  updated_at timestamptz not null default now()
);

-- Server-issued rotating sessions. The httpOnly `sid` cookie is the working
-- credential (not the raw code). Rotation + reuse detection make a copied cookie
-- jar fight with its origin: only one session per device_id stays active, so a
-- shared/cloned credential is usable by one client at a time. See session.js.
create table if not exists sessions (
  sid        text primary key,
  code       text not null references access_codes(code) on delete cascade,
  device_id  text not null,                        -- server-generated, never exposed to the client
  active     boolean not null default true,
  created_at timestamptz not null default now(),
  last_seen  timestamptz not null default now(),
  rotated_at timestamptz
);
create index if not exists idx_sessions_code on sessions(code);
create index if not exists idx_sessions_device_active on sessions(device_id, active);

-- private question bank (served from DB, not from the public repo URL). See DATA_SOURCE=db.
create table if not exists bank (
  num        int primary key,
  data       jsonb not null,
  updated_at timestamptz not null default now()
);

-- editable app config (brand name, price...). No redeploy needed to change.
create table if not exists settings (
  key        text primary key,
  value      text not null,
  updated_at timestamptz not null default now()
);

-- Free-trial leads: an email captured before the 10-question sampler. Lets us
-- measure conversion (a paid purchase whose email also appears here = a lead that
-- converted). Deduped by email; source records where the signup came from.
create table if not exists trial_leads (
  id         serial primary key,
  email      text not null unique,
  anon_id    text,                 -- random client id, ties repeat visits together
  source     text,                 -- e.g. landing-hero, landing-price, app
  created_at timestamptz not null default now()
);
create index if not exists idx_trial_leads_created on trial_leads(created_at);

create table if not exists coupons (
  code        text primary key,
  kind        text not null default 'percent',     -- percent | fixed | full (free access, no checkout)
  value       numeric(10,2) not null,
  partner_ref text,
  active      boolean not null default true,
  max_uses    int,
  uses        int not null default 0,
  created_at  timestamptz not null default now()
);
