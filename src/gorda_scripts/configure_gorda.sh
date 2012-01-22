1. Create a database cluster which is a collection of databases managed by a single server instance:

$gorda/install/pgsql/bin/initdb -D $gorda/PostgreSQL.data.1

2. After creating a database cluster, run the PostgreSQL as follows:

$gorda/install/pgsql/bin/postmaster -i -p 5432 \

-D $gorda/PostgreSQL.data.1

3. Change to the directory src/reflector/scripts and create a database as follows:

$gorda/install/pgsql/bin/createdb test

4. Create a set of tables to be replicated. To do so, ﬁrstly, run the PostgreSQL utility psql as follows:

$gorda/install/pgsql/bin/psql -d test

5. Then type the following SQL commands to create tables:

create sequence seqorders increment by 1 no minvalue

no maxvalue start with 1 cache 20 no cycle;

create table orders (key int not null default

nextval(’seqorders’), sum float, description varchar(20),

primary key (key));




create table order_line (key int not null default nextval(’seqorderline’), okey int, value float, unit int, description varchar(20), primary key (key));



