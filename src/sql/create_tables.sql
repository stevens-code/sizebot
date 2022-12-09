-- Emoji to variable association table
CREATE TABLE emoji_variables(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
emoji           TEXT        NOT NULL,
variable_name   TEXT        NOT NULL
);

-- Keep stats of who shrunk/grew who
CREATE TABLE sizeray_actions(
guild           INT         NOT NULL,
timestamp       TIMESTAMP   NOT NULL,
action          TEXT        NOT NULL,
target          INT         NOT NULL,
author          INT         NOT NULL
);

-- Keep track of sizeray immunity
CREATE TABLE sizeray_immunity(
guild         INT         NOT NULL,
timestamp     TIMESTAMP   NOT NULL,
target        INT         NOT NULL
);