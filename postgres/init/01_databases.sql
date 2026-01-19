CREATE ROLE catalog_user WITH LOGIN PASSWORD 'catalog_pass';
CREATE ROLE auth_user WITH LOGIN PASSWORD 'auth_pass';
CREATE ROLE booking_user WITH LOGIN PASSWORD 'booking_pass';
CREATE ROLE seance_user WITH LOGIN PASSWORD 'seance_pass';

CREATE DATABASE catalog_db OWNER catalog_user;
CREATE DATABASE auth_db OWNER auth_user;
CREATE DATABASE booking_db OWNER booking_user;
CREATE DATABASE seance_db OWNER seance_user;

GRANT ALL PRIVILEGES ON DATABASE catalog_db TO catalog_user;
GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;
GRANT ALL PRIVILEGES ON DATABASE booking_db TO booking_user;
GRANT ALL PRIVILEGES ON DATABASE seance_db TO seance_user;
