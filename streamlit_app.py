import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Connect to PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:Amazonaws@gouthamdb.cjsam84ckn23.ap-south-1.rds.amazonaws.com:5432/postgres')

# Title
st.title("Sales Analysis Dashboard")

# Query data
query = "SELECT p.product_id, SUM(o.sale_price) AS total_revenue FROM order_data o join product_data p on p.product_id = o.product_id GROUP BY p.product_id ORDER BY total_revenue DESC LIMIT 10;"
df = pd.read_sql(query, engine)

# Display table
st.header("Top 10 Revenue-Generating Products")
st.dataframe(df)

# Display chart
st.bar_chart(df.set_index('product_id')['total_revenue'])

#Top 5 Profit Powerhouses: Cities That Excel in Margins

# Query data
query = "select city,avg(case when sale_price = 0 then 0 else ((profit/sale_price)*100) end) as profit_margin from order_data group by city order by profit_margin desc limit 5;"
df = pd.read_sql(query, engine)

# Display table
st.header("Top 5 Profit Powerhouses: Cities That Excel in Margins")
st.dataframe(df)

# Display chart
st.bar_chart(df.set_index('city')['profit_margin'])

