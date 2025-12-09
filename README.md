the dotenv consists of
SUPABASE_KEY = 'your_key'
SUPABASE_URL = 'your_url'

### SQl
CREATE TABLE titanic_data (
    id BIGSERIAL PRIMARY KEY,

    survived INTEGER,
    pclass INTEGER,
    sex TEXT,
    age FLOAT,
    sibsp INTEGER,
    parch INTEGER,
    fare FLOAT,
    embarked TEXT,
    class TEXT,
    who TEXT,
    adult_male INTEGER,
    deck TEXT,
    embark_town TEXT,
    alive TEXT,
    alone INTEGER,

    family_size INTEGER,
    is_alone INTEGER,
    is_child INTEGER,
    age_bin TEXT,
    fare_per_person FLOAT,
    fare_bin TEXT,

    sex_male INTEGER,
    sex_female INTEGER,

    embarked_C INTEGER,
    embarked_Q INTEGER,
    embarked_S INTEGER
);
