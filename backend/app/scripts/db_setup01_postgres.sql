-- ============================================================
-- DB SETUP 01: ADMIN USER
-- 1) Run as postgres superuser on fioapi_db
-- 2) Create fioapi_admin user. Grant necessary privileges.
-- ============================================================

-- Create a database-specific admin (PoLP)
CREATE USER fioapi_admin WITH PASSWORD 'your_admin_password';
GRANT CONNECT ON DATABASE fioapi_db TO fioapi_admin;
-- Lets admin modify db itself
GRANT ALL PRIVILEGES ON DATABASE fioapi_db TO fioapi_admin;
ALTER DATABASE fioapi_db OWNER TO fioapi_admin;
-- Lets admin modify public schema within fioapi_db
GRANT ALL PRIVILEGES ON SCHEMA public TO fioapi_admin;
ALTER SCHEMA public OWNER TO fioapi_admin;
ALTER USER fioapi_admin WITH CREATEROLE;

-- Verify fioapi_admin is created
SELECT usename FROM pg_user WHERE usename = 'fioapi_admin';