create table offers_x5
(
    id SERIAL,
    name_pr TEXT,
    price_now TEXT,
    price_old TEXT,
    brand TEXT,
    made_in TEXT,
    expiration_date TEXT,
    weight_pr TEXT
);

create table offers_magnit
(
    id SERIAL,
    name_pr TEXT,
    price_now TEXT,
    price_old TEXT,
    brand TEXT,
    made_in TEXT,
    expiration_date TEXT,
    weight_pr TEXT
);

create table users_id(
    db_id SERIAL, 
    user_id TEXT PRIMARY KEY
);