CREATE TABLE bioobject(
    id SERIAL,
    uuid TEXT UNIQUE,
    PRIMARY KEY id
);

CREATE TABLE analysis(
    bioobject_id INT,
    path TEXT UNIQUE,
    data JSONB,
    FOREIGN KEY id REFERENCES bioobject(id)
);

