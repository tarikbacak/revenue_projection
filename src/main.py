import streamlit as st
from services.projection_service import ProjectionService
from components.sidebar import render_sidebar
from components.metrics import display_metrics
from components.charts import plot_revenue_chart, plot_users_chart
from components.data_table import display_projections_table

def main():
    st.set_page_config(page_title="Revenue Projection Tool", layout="wide")
    st.title("Revenue Projection Tool")
    
    projection_service = ProjectionService()
    
    # Render sidebar
    render_sidebar(projection_service)
    
    try:
        # Calculate projections
        projections = projection_service.calculate_projections(months=12)
        
        # Display metrics
        display_metrics(projections)
        
        # Display charts
        plot_revenue_chart(projections, projection_service)
        plot_users_chart(projections, projection_service)
        
        # Display data table
        display_projections_table(projections, projection_service)
        
    except Exception as e:
        st.error(f"Error calculating projections: {str(e)}")

if __name__ == "__main__":
    main() 