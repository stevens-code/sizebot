-- Table to store guild-specific variables 
CREATE TABLE text_variables(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
variable_name   TEXT        NOT NULL,
variable_value  TEXT        NOT NULL
);

-- Keep stats of size ray actions
-- Includes who shrunk/grew who and size ray shields
-- The a member's current state is equal to the latest size ray 
-- action where they are the target
CREATE TABLE sizeray_actions(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
action          TEXT        NOT NULL,
target          INT         NOT NULL,
author          INT         NOT NULL
);

-- Store the size ray immunity role for each guild
CREATE TABLE sizeray_immunity_roles(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
role            INT         NOT NULL
);