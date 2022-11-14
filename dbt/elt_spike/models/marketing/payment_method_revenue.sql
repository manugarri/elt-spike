with orders as (

    select * from {{ ref('stg_orders') }}

),

payments as (

    select * from {{ ref('stg_payments') }}

),

order_payments as (

    select
        order_id,
        payment_method,
        sum(amount) as total_amount

    from payments

    group by order_id, payment_method
),

final as (

    select
        orders.order_date as date,
        payment_method,
        sum(order_payments.total_amount) as revenue
    from orders

    left join order_payments
        on orders.order_id = order_payments.order_id

    where orders.status = 'completed'
    group by date, payment_method
)

select * from final