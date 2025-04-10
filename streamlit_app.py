import streamlit as st
import pg8000
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Connect to the database
def create_connection():
        connection = pg8000.connect(
            host="database-1.cdsce8eqs025.ap-south-1.rds.amazonaws.com",
            database="postgres",
            user="postgres",
            password="Amazonaws",
            port="5432"
        )
        return connection
    
def run_query(query):
    connection=create_connection()
    if connection is None:
        return None
    try:
        df = pd.read_sql_query(query, connection)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        connection.close()
    
# Streamlit app for running SQL queries
def main():
    st.sidebar.title("Retail Order Data Analysis ")

guvi_queries = {
    "Top 10 highest revenue generating products": 
        "select p.product_id,p.sub_category,sum(o.sale_price) as revenue from product_data p join order_data o on p.product_id=o.product_id group by p.product_id,p.sub_category order by revenue desc limit 10;",
    
    "Top 5 cities with the highest profit margins": 
        "select city,avg(case when sale_price = 0 then 0 else ((profit/sale_price)*100) end)as profit_margin from order_data group by city order by profit_margin desc limit 5;",
    
    "Total discount given for each category": 
        "select p.category,sum(o.discount_amount*o.quantity) as total_discount from product_data p join order_data o on p.product_id=o.product_id group by p.category;",
    
    "Average sales price per product category": 
       "select p.category,avg(o.sale_price) as Avg_saleprice from order_data o join product_data p on p.product_id= o.product_id group by category;",
    
    "The highest average sale price":
       "select region, avg(sale_price) as avg_sales from order_data group by region order by avg_sales desc limit 1 ;",
    
    "Total profit per category": 
       "select p.category, sum(o.profit) as total_profit from product_data p join order_data o on p.product_id=o.product_id group by p.category;",
    
    "Top 3 segments with the highest quantity of orders": 
        "select segment, sum(quantity) as highest_quantity  from order_data group by segment order by highest_quantity desc;",
    
    "Average discount percentage given per region": 
        "select region, round(avg(discount_percent),2) as avg_discount from order_data group by region;",
    
    "Product category with the highest total profit": 
        "select p.category, round(sum(o.profit)::numeric,2) as total_profit from product_data p join order_data o on p.product_id=o.product_id group by p.category order by total_profit desc limit 1;",

   "Total revenue generated per year": 
       "select order_year, round(sum(sale_price)::numeric,2) as Revenue_per_year from order_data group by order_year;",
}

my_queries={

        "Identify the 10 products with the highest quantity sold, including their total revenue and profit":
    "select p.product_id, p.category, sum(o.quantity) as Total_quantity, round(sum(o.sale_price)::numeric,2) as Revenue, round(sum(o.profit)::numeric,2) as profit from product_data p join order_data o on p.product_id=o.product_id group by p.product_id,p.category order by sum(o.quantity) desc limit 10;",

     "Determine the top 5 states with the highest total sales revenue with category.":
    "select o.state, p.product_id,p.category,round(sum(o.sale_price)::numeric,2) from order_data o join product_data p on o.product_id=p.product_id group by o.state,p.product_id,p.category order by sum(sale_price) desc limit 5;",
"Count the total number of orders placed for each product category, include the quantity and revenue":
"select p.category,sum(o.order_id) as order_count,o.quantity,round(sum(o.sale_price)::numeric,2) as revenue from product_data p join order_data o on p.product_id=o.product_id group by p.category,o.quantity;",
"Rank all regions based on the total quantity of products sold include order count":
"select o.region, sum(o.quantity) as total_quantity, count(o.order_id) as order_count,rank() over(order by sum(quantity) desc) from order_data o join product_data p on p.product_id=o.product_id group by o.region;",

"Identify the Top 3 Customers by Total Profit Contribution":
"select segment, round(sum(profit)::numeric,2) as profit, rank() over(order by sum(profit) desc) from order_data group by segment;",

"Find the Month with the Highest Revenue":
"select order_month, round(sum(sale_price)::numeric,2) as profit,rank() over(order by sum(sale_price) desc) from order_data group by order_month;",

"Calculate the Average Order Quantity by Product":
"select p.sub_category, round(avg(o.quantity),2) as Avg_quantity,count(o.order_id) from product_data p join order_data o on o.product_id=p.product_id group by p.sub_category;",

"Analyze the Total Revenue Generated by Each Segment":
"select segment, round(sum(sale_price)::numeric,2) as total_revenue from order_Data group by segment;",

"calculate the total profit for the all the region":
"select region, round(sum(profit)::numeric,2) from order_Data group by region order by sum(profit) desc;",

"find which state ordered high quantity through which shipping mode":
"select state, sum(quantity) as Total_quanity, ship_mode from order_data group by state,ship_mode order by sum(quantity) desc;"

}
Business_Insights={
    "Top-Selling Products":
        "select p.product_id,p.sub_category,sum(o.sale_price),rank() over(order by sum(o.sale_price) desc) as rank from product_data p join order_data o on p.product_id=o.product_id group by p.product_id,p.sub_category;",
"Monthly Sales Analysis":
"Select order_year, order_month, SUM(sale_price) AS total_sales FROM order_data GROUP BY order_year, order_month ORDER BY order_year, order_month;",
"Product Performance":
"SELECT product_id, SUM(sale_price) AS total_revenue, SUM(profit) AS total_profit, CASE WHEN SUM(profit)/NULLIF(SUM(sale_price), 0) > 0.2 THEN 'High Margin' ELSE 'Low Margin' END AS profit_category, ROW_NUMBER() OVER(ORDER BY SUM(sale_price) DESC) AS rank FROM order_data GROUP BY product_id HAVING SUM(sale_price) > 0 ORDER BY total_revenue DESC;",
"Regional Sales Analysis":
"SELECT region, SUM(sale_price) AS total_sales FROM order_data GROUP BY region ORDER BY total_sales DESC;",
"Discount Analysis":
"select product_id,sum(quantity) as total_quantity,sum(discount_percent) as Total_D_percent, round(sum(discount_amount)::numeric,2) as total_discount, round(sum(sale_price)::numeric,2) as total_sale, round((sum(discount_amount)::numeric/ sum(sale_price)::numeric)* 100,2) as discountimpactpercentage from order_data  group by product_id having sum(discount_percent)>20 order by discountimpactpercentage desc;"
}
# Navigation options
nav = st.sidebar.radio("Select Query Section",["Guvi Queries" , "My Queries","Business Insights"])

# Query selection based on navigation
if nav == "Guvi Queries":
    st.subheader("Guvi Queries")
    query = st.selectbox("Select a query to visualize:", list(guvi_queries.keys()))
    selected_query_set = guvi_queries
elif nav == "My Queries":
    st.subheader("My Queries")
    query = st.selectbox("Select a query to visualize:", list(my_queries.keys()))
    selected_query_set = my_queries
elif nav == "Business Insights":
    st.subheader("Business Insights")
    query = st.selectbox("Select a query to visualize:", list(Business_Insights.keys()))
    selected_query_set = Business_Insights
else:
    query = None

# Execute and visualize selected query
if query:
    result_df = run_query(selected_query_set[query])
    if result_df is not None:
        st.dataframe(result_df)

 
         # Dynamic Visualization based on result_df columns
        if "revenue" in result_df.columns or "total_sales" in result_df.columns:
            col_name = "revenue" if "revenue" in result_df.columns else "total_sales"
            st.bar_chart(result_df.set_index(result_df.columns[0])[col_name])
        elif "profit_margin" in result_df.columns:
            st.line_chart(result_df.set_index(result_df.columns[0])["profit_margin"])
        elif "total_discount" in result_df.columns and "total_sale" in result_df.columns:
            st.subheader("Discount vs Sales Analysis")
            fig = px.scatter(result_df, x="total_discount", y="total_sale", size="total_quantity", color="product_id", title="Impact of Discounts on Sales")
            st.plotly_chart(fig)
        elif "total_quantity" in result_df.columns and "profit" in result_df.columns:
            st.subheader("Quantity vs Profit Analysis")
            fig = px.bar(result_df, x="product_id", y="total_quantity", color="profit", title="Top Products by Quantity and Profit")
            st.plotly_chart(fig)
        elif "order_month" in result_df.columns:
            st.line_chart(result_df.set_index("order_month")["profit"])
        elif "state" in result_df.columns:
            st.subheader("State-wise Analysis")
            fig = px.bar(result_df, x="state", y=result_df.columns[2], color="state", title="Top States by Revenue or Quantity")
            st.plotly_chart(fig)
        elif "category" in result_df.columns and "total_discount" in result_df.columns:
            st.subheader("Category Discount Analysis")
            fig = px.pie(result_df, names="category", values="total_discount", title="Total Discount Given per Category")
            st.plotly_chart(fig)
        elif "segment" in result_df.columns and "total_sales" in result_df.columns:
            st.subheader("Segment Sales Analysis")
            fig = px.line(result_df, x="segment", y="total_sales", title="Sales Trend per Segment")
            st.plotly_chart(fig)
        elif "product_id" in result_df.columns and "total_profit" in result_df.columns:
            st.subheader("Product Profit Analysis")
            fig = px.bar(result_df, x="product_id", y="total_profit", color="total_profit", title="Profit per Product")
            st.plotly_chart(fig)
        elif "order_year" in result_df.columns and "total_sales" in result_df.columns:
            st.subheader("Yearly Sales Analysis")
            fig = px.bar(result_df, x="order_year", y="total_sales", color="order_year", title="Sales Trend Over Years")
            st.plotly_chart(fig)
        elif "product_id" in result_df.columns and "total_quantity" in result_df.columns:
            st.subheader("Product Quantity Analysis")
            fig = px.scatter(result_df, x="product_id", y="total_quantity", size="total_quantity", title="Quantity of Products Sold")
            st.plotly_chart(fig)
        elif "category" in result_df.columns and "quantity" in result_df.columns:
            st.subheader("Category Quantity Analysis")
            fig = px.bar(result_df, x="category", y="quantity", color="category", title="Quantity Sold per Category")
            st.plotly_chart(fig)
        else:
            st.warning("No specific visualization template available for this query.")
