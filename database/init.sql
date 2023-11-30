create table offers
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

INSERT INTO offers (name_pr, price_now, price_old, brand, made_in, expiration_date, weight_pr)

VALUES ('1', '1', '1', '1', '1', '1', '1'), 
        ('12', '12', '12', '12', '12', '12', '12');