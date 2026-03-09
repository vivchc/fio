-- ============================================================
-- DB SETUP 02: MIGRATION AND RUNTIME USERS
-- 1) Run as fioapi_admin user on fioapi_db
-- 2) Create migration and runtime user. Grant necessary privileges.
-- ============================================================

-- Create migration + runtime users for PoLP
CREATE USER fioapi_migration WITH PASSWORD 'your_migration_password';
CREATE USER fioapi_runtime WITH PASSWORD 'your_runtime_password';

GRANT USAGE, CREATE ON SCHEMA public TO fioapi_migration;
GRANT USAGE ON SCHEMA public TO fioapi_runtime;

-- Grants migration user full access to tables and sequences it creates
ALTER DEFAULT PRIVILEGES FOR ROLE fioapi_migration IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO fioapi_migration;
ALTER DEFAULT PRIVILEGES FOR ROLE fioapi_migration IN SCHEMA public
GRANT ALL PRIVILEGES ON SEQUENCES TO fioapi_migration;

-- For tables created by migration user, grants runtime user read/write permissions
ALTER DEFAULT PRIVILEGES FOR ROLE fioapi_migration IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO fioapi_runtime;

-- For tables created by migration user, lets runtime user insert rows
ALTER DEFAULT PRIVILEGES FOR ROLE fioapi_migration IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO fioapi_runtime;

-- Verify migration runtime users are created
SELECT usename FROM pg_user WHERE usename LIKE 'fioapi%' AND usename != 'fioapi_admin';