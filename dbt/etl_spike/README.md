Data modeled based on jaffle_shop tutorial
https://github.com/dbt-labs/jaffle_shop/blob/main/models/schema.yml


###
DBT Snapshots
I based the snapshots on this tutorial 
https://www.startdataengineering.com/post/dbt-data-build-tool-tutorial/#332-snapshots
basically:
  1.we run a initial snapshot for the raw_customers source (run `dbt snapshot`),
  2.update a existing customer with 
    ```
    UPDATE public.raw_customers
     SET first_name='UPDATED_NAME'
     WHERE id=1
    ;
    ```
  3.Run dbt snapshot and dbt run (we dont need the run if the core models are views)
  4.Now we can check the output on the staging table:
  ```
    dbt=# select * from public.stg_customers where customer_id=1;
    customer_id |  first_name  | last_name |       dbt_valid_from       |        dbt_valid_to
    -------------+--------------+-----------+----------------------------+----------------------------
            1 | Michael      | P.        | 2022-10-18 10:52:12.793064 | 2022-10-18 11:03:33.663161
            1 | UPDATED_NAME | P.        | 2022-10-18 11:03:33.663161 |
    (2 rows)
  ```
  5.add a new customer:
  ```
  INSERT INTO public.raw_customers VALUES  (101,'manuel','garrido');
  ```
  6.run a new snapshot *dbt snapshot and dbt run)
  7.Now we can check the output
  ```
    dbt=# select * from public.stg_customers where customer_id in (1,101);
    customer_id |  first_name  | last_name |       dbt_valid_from       |        dbt_valid_to
    -------------+--------------+-----------+----------------------------+----------------------------
            1 | Michael      | P.        | 2022-10-18 10:52:12.793064 | 2022-10-18 11:03:33.663161
            1 | UPDATED_NAME | P.        | 2022-10-18 11:03:33.663161 |
            101 | manuel       | garrido   | 2022-10-18 11:08:26.04012  |
    (3 rows)
  ```

Used commands
- `dbt seed`, run once, to seed the raw source tables
- `dbt snapshot`, to generate snapshots, run before every dbt run
- `dbt run`, to update tables based on model updates
- `dbt test`, to run tests, run after every dbt run
- `dbt docs generate` to generate docs and `dbt docs serve` to show them



### Notes

model files cant share the name across all folders, thats why we add prefixes to them (so models inside `staging` start with prefix `stg_`)


### Resources:

DBT tests practices
https://www.datafold.com/blog/7-dbt-testing-best-practices
