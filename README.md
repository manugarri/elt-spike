ETL Spike

This spike uses a dummy dataset for a store to demonstrate how Prefect (scheduler), DBT (sql execution) and Great expectations can work together.

You can see the initial csv datasets in the folder `./dbt/etl_spike/seeds`
# Setup
You need docker-compose (and psql locally if you want to interact with the database)

`make up` To spin up the environment.


## DBT Setup
once that is done you can run these commands **just once** to populate the initial sources (tables) that the ELT will read from:

```
dbt seed
dbt snapshot
``` 


## Great expectations Setup

echo 'dbpassword: password1234' > great_expectations/uncommitted/config_variables.yml                                                      

build initial datadocs:

```
make great_expectations
  great_expectations docs build
```

---

# Prefect ETL
run etl:
```
make prefect-cli
  python etl_flow.py
```

# Snapshots

Snapshots are a good way to track slowly changing dimensions. For example, names/addressess for people/businesses.

We can show an example easily. 

We can open connect to the postgres data warehouse:

```make psql```

Then check the data for a customer:

```
select * from carpe.customers where customer_id=1;
```

Which should return the following:

```
dbt=# dbt=# select * from public.customers where customer_id=1;
 customer_id | first_name | last_name | first_order | most_recent_order | number_of_orders | customer_lifetime_value 
-------------+------------+-----------+-------------+-------------------+------------------+-------------------------
           1 | Michael    | P.        | 2018-01-01  | 2018-02-10        |                2 |                      33

```

Now lets say the source data has changed, we ingest a source  again and where these 2 events have happened:
- the name for this particular customer (id=1) has changed.
- there is a new customer 

We can recreate these event via the following sql commands. Please notice we are updating the sources table (which includes the seeded data that represents the sources):

```
  UPDATE public.raw_customers
     SET first_name='UPDATED_NAME'
     WHERE id=1
;
```
and 

```
  INSERT INTO public.raw_customers VALUES  (101,'manuel','garrido');

```

Now lets run the etl again (so `make prefect-cli` and then `python elt_flow.py`)

Lets see how the customer table looks like now:

```
dbt=# select * from public.customers where customer_id in (1,101);
 customer_id |  first_name  | last_name | first_order | most_recent_order | number_of_orders | customer_lifetime_value 
-------------+--------------+-----------+-------------+-------------------+------------------+-------------------------
           1 | UPDATED_NAME | P.        | 2018-01-01  | 2018-02-10        |                2 |                      33
         101 | manuel       | garrido   |             |                   |                  |                        
(2 rows)


```

It all makes sense right? we can see the new customer and the existing customer has the updated name.

But what if we wanted to know the customer's name history? FRET NOT, snapshots to the rescue!

Since we have snapshots at the source, and the staging table reads from snapshots, we can see how the staging table actually looks now:

```
Now we can check the output
  ```
    dbt=# select * from public.stg_customers where customer_id in (1,101);
    customer_id |  first_name  | last_name |       dbt_valid_from       |        dbt_valid_to
    -------------+--------------+-----------+----------------------------+----------------------------
            1 | Michael      | P.        | 2022-10-18 10:52:12.793064 | 2022-10-18 11:03:33.663161
            1 | UPDATED_NAME | P.        | 2022-10-18 11:03:33.663161 |
            101 | manuel       | garrido   | 2022-10-18 11:08:26.04012  |
    (3 rows)
```



### Prefect Deployment

Remote DAG deployment
We can use minio to mimic s3 for flow deployment.

Create a Minio bucket
go to http://minio:9001
login with `minioadmin` user and password
create a bucket named prefect-flows

Create a Prefect Remote File block.
on prefect UI go to blocks, then search for remote file system block.

block name: minio
path: s3://prefect-flows/deployments

Settings (Optional):
{
  "key": "minioadmin",
  "secret": "minioadmin",
  "client_kwargs": {
    "endpoint_url": "http://minio:9000"
  }
}

prefect deployment build test.py:test -n test -q default -sb remote-file-system/minio
prefect deployment apply test-deployment.yaml

you can now trigger it via the ui!


prefect deployment build flows/elt_flow.py:elt_flow -n elt -q default -sb remote-file-system/minio
prefect deployment apply elt_flow-deployment.yaml