import psycopg2

# create a connection to the Postgres database
conn = psycopg2.connect(
    host="localhost",
    database="sunday1",
    user="postgres",
    password="12345"
)

# create a cursor object to interact with the database
cur = conn.cursor()

# create the user table
cur.execute('''
    CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(255) UNIQUE NOT NULL,
      email VARCHAR(255) UNIQUE NOT NULL,
      password_hash VARCHAR(255) NOT NULL,
      is_superuser BOOLEAN NOT NULL DEFAULT false,
      is_active BOOLEAN NOT NULL DEFAULT true,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      CONSTRAINT is_superuser_check CHECK (is_superuser IN (TRUE, FALSE))
    );
''')

# create the tenant table
cur.execute('''
    CREATE TABLE tenant (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) UNIQUE NOT NULL,
      domain_name VARCHAR(255) UNIQUE NOT NULL,
      api_key VARCHAR(255) UNIQUE NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')



# create the role table
cur.execute('''
    CREATE TABLE role (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) UNIQUE NOT NULL,
      description VARCHAR(255) NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')

# create the tenant_user table
cur.execute('''
    CREATE TABLE tenant_user (
      id SERIAL PRIMARY KEY,
      user_id INTEGER NOT NULL REFERENCES users(id),
      tenant_id INTEGER NOT NULL REFERENCES tenant(id),
      role_id INTEGER NOT NULL REFERENCES role(id),
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')

# create the module table
cur.execute('''
    CREATE TABLE module (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description VARCHAR(255) NOT NULL,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')

# create the submodule table
cur.execute('''
    CREATE TABLE submodule (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description VARCHAR(255) NOT NULL,
      module_id INTEGER NOT NULL REFERENCES module(id),
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')

# create the microservice table
cur.execute('''
    CREATE TABLE microservice (
      id SERIAL PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      description VARCHAR(255) NOT NULL,
      url VARCHAR(255) NOT NULL,
      submodule_id INTEGER NOT NULL REFERENCES submodule(id),
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
''')

# create the project_module table
cur.execute('''
    CREATE TABLE project_module (
      id SERIAL PRIMARY KEY,
      module_id INTEGER NOT NULL REFERENCES module(id),
      project_id INTEGER NOT NULL REFERENCES tenant(id)
    );
''')

# create the project_submodule table
cur.execute('''
    CREATE TABLE project_submodule (
      id SERIAL PRIMARY KEY,
      submodule_id INTEGER NOT NULL REFERENCES submodule(id),
      project_id INTEGER NOT NULL REFERENCES tenant(id)
    );
''')

# create the project_microservice table
cur.execute('''
    CREATE TABLE project_microservice (
      id SERIAL PRIMARY KEY,
      microservice_id INTEGER NOT NULL REFERENCES microservice(id),
      project_id INTEGER NOT NULL REFERENCES tenant(id)
    );
''')

# add foreign key constraints to tenant_user table
cur.execute('''
    ALTER TABLE tenant_user
    ADD CONSTRAINT user_id_fk
    FOREIGN KEY (user_id)
    REFERENCES users(id);
''')

cur.execute('''
    ALTER TABLE tenant_user
    ADD CONSTRAINT tenant_id_fk
    FOREIGN KEY (tenant_id)
    REFERENCES tenant(id);
''')

cur.execute('''
    ALTER TABLE tenant_user
    ADD CONSTRAINT role_id_fk
    FOREIGN KEY (role_id)
    REFERENCES role(id);
''')

# add foreign key constraints to project_module table
cur.execute('''
    ALTER TABLE project_module
    ADD CONSTRAINT module_id_fk
    FOREIGN KEY (module_id)
    REFERENCES module(id);
''')

cur.execute('''
    ALTER TABLE project_module
    ADD CONSTRAINT project_id_fk
    FOREIGN KEY (project_id)
    REFERENCES tenant(id);
''')

# add foreign key constraints to project_submodule table
cur.execute('''
    ALTER TABLE project_submodule
    ADD CONSTRAINT submodule_id_fk
    FOREIGN KEY (submodule_id)
    REFERENCES submodule(id);
''')

cur.execute('''
    ALTER TABLE project_submodule
    ADD CONSTRAINT project_id_fk
    FOREIGN KEY (project_id)
    REFERENCES tenant(id);
''')

# add foreign key constraints to project_microservice table
cur.execute('''
    ALTER TABLE project_microservice
    ADD CONSTRAINT microservice_id_fk
    FOREIGN KEY (microservice_id)
    REFERENCES microservice(id);
''')

cur.execute('''
    ALTER TABLE project_microservice
    ADD CONSTRAINT project_id_fk
    FOREIGN KEY (project_id)
    REFERENCES tenant(id);
''')

# add a unique constraint to role table
cur.execute('''
    ALTER TABLE role
    ADD CONSTRAINT role_name_unique
    UNIQUE (name);
''')

# commit the changes and close the cursor and connection
conn.commit()
cur.close()
conn.close()
