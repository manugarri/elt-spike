{% snapshot raw_customers_snapshot %}

    {{
        config(
          target_schema='snapshots',
          strategy='check',
          unique_key='id',
          invalidate_hard_deletes=True,
          check_cols='all'
        )
    }}

    select * from {{ source('public', 'raw_customers') }}

{% endsnapshot %}