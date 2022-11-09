ETL Spike


`make up` To spin up the environment.

once that is done you can run these commands **just once** to populate the initial sources (tables) that the ELT will read from:

```
dbt seed
dbt snapshot
``` 


Great expectations

echo 'dbpassword: password1234' > great_expectations/uncommitted/config_variables.yml                                                      