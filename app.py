import streamlit as st
import pandas as pd
import pickle


st.set_page_config(
    page_title="Customer Attrition Predictor",
    page_icon="📊",
    layout="wide"
)


with open('churn_model.pkl', 'rb') as file:
    model = pickle.load(file)


st.markdown("""
    <div style="text-align: center;">
        <h1 style="margin-bottom: 5px;">📊 Enterprise Customer Attrition Predictor</h1>
        <p style="font-size: 18px; color: #555; margin-top: 0;">Upload your customer database (CSV) to instantly detect high-risk and lapsing customers.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")


uploaded_file = st.file_uploader("Upload Customer RFM Data (CSV File)", type=["csv"])

if uploaded_file is not None:
    
    
    input_df = pd.read_csv(uploaded_file)
    
    
    required_cols = ['Recency', 'Frequency', 'Monetary']
    if all(col in input_df.columns for col in required_cols):
        
        
        features = input_df[required_cols]
        input_df['Churn_Prediction'] = model.predict(features)
        
        
        input_df['Status'] = input_df['Churn_Prediction'].map({1: '⚠️ At Risk', 0: '✅ Active / Loyal'})
        
        st.success("🎉 Analysis Complete!")
        st.write("### 📈 Executive Summary")
        
      
        total_customers = len(input_df)
        attrition_count = len(input_df[input_df['Churn_Prediction'] == 1])
        risk_percentage = (attrition_count / total_customers) * 100
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #4682B4;">
                <p style="margin: 0; font-size: 16px; color: #555;">Total Customers Scanned</p>
                <h2 style="margin: 0; font-size: 32px; color: #1E3A8A;">{total_customers:,}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div style="background-color: #fde8e8; padding: 20px; border-radius: 10px; border-left: 5px solid #e11d48;">
                <p style="margin: 0; font-size: 16px; color: #555;">Customers At Attrition Risk</p>
                <h2 style="margin: 0; font-size: 32px; color: #991B1B;">{attrition_count:,} <span style="font-size: 18px; color: #DC2626;">({risk_percentage:.1f}% Risk)</span></h2>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True) 
        
       
        st.subheader("🚨 High-Risk & Lapsing Customers List")
        risk_customers = input_df[input_df['Churn_Prediction'] == 1][['Recency', 'Frequency', 'Monetary', 'Status']]
        
        if not risk_customers.empty:
            
            st.dataframe(risk_customers, use_container_width=True)
            
          
            csv = risk_customers.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Targeted Retention List (CSV)",
                data=csv,
                file_name="high_attrition_risk_customers.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Awesome! No high-risk customer attrition detected.")
            
    else:
        st.error("Error: The uploaded CSV file must contain 'Recency', 'Frequency', and 'Monetary' columns.")