with source as (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from {{ ref('raw_customers_snapshot') }}

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name,
        dbt_valid_from,
        dbt_valid_to

    from source

)

select * from renamed