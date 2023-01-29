-- Table to store guild-specific variables 
CREATE TABLE IF NOT EXISTS text_variables(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
variable_name   TEXT        NOT NULL,
variable_value  TEXT        NOT NULL
);

-- Keep stats of size ray actions
-- Includes who shrunk/grew who and size ray shields
-- The a member's current state is equal to the latest size ray 
-- action where they are the target
CREATE TABLE IF NOT EXISTS sizeray_actions(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
action          TEXT        NOT NULL,
target          INT         NOT NULL,
author          INT         NOT NULL
);

-- Store the size ray immunity role for each guild
CREATE TABLE IF NOT EXISTS sizeray_immunity_roles(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
role            INT         NOT NULL
);

-- If a guild has an entry, welcome messages are disabled
CREATE TABLE IF NOT EXISTS greeter_disable_welcome(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL
);

-- If a guild has an entry, goodbye messages are disabled
CREATE TABLE IF NOT EXISTS greeter_disable_goodbye(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL
);

-- If a guild has an entry, birthday messages are disabled
CREATE TABLE IF NOT EXISTS birthday_disable(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL
);

-- Settings to fetch the birthday data from Google Sheets
CREATE TABLE IF NOT EXISTS birthday_settings(
guild                   INT         NOT NULL,
timestamp               TIMESTAMP   NOT NULL,
sheets_key              TEXT        NOT NULL,
sheets_name_column      TEXT        NOT NULL,
sheets_birthday_column  TEXT        NOT NULL
);

-- Message to tell users where to put their birthdays
-- (link to Google Sheets/Forms)
CREATE TABLE IF NOT EXISTS birthday_source_info(
guild       INT         NOT NULL,
timestamp   TIMESTAMP   NOT NULL,
info        TEXT        NOT NULL
);

-- Store birthdays for each guild
CREATE TABLE IF NOT EXISTS birthdays(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
name            TEXT        NOT NULL,
month           INT         NOT NULL,
day             INT         NOT NULL
);

-- Store a custom channel for the bot
CREATE TABLE IF NOT EXISTS notifications_channel(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
channel         INT         NOT NULL
);

-- Store user names and avatars
CREATE TABLE IF NOT EXISTS member_cache(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
id              INT         NOT NULL,
name            TEXT        NOT NULL,
avatar          TEXT        NOT NULL
);