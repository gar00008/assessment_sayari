import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib, json
import time
from datetime import datetime, timedelta


curr_time = (datetime.now()-timedelta(hours=5)).strftime("%a, %b %d %Y %H:%M:%S")

import sc_kb_data as scd
import sc_kb_figure as scf

data,labels = scd.get_risk_data()
nodes,links = scd.get_sc_data()
notes = scd.get_notes()

st.set_page_config(layout="wide")
#st.title('Assent Knowledgebase')
st.caption('version: '+ curr_time)

products = []
products.extend(data['product'].unique())
risks = []
risks.extend(['e-climate_impact', 'e-biodiversity', 's-human_trafficking','s-labor_rights', 'g-org_commitment', 'g-resiliency'])
suppliers = []
suppliers.extend(data['supplier'].unique())
years = [2022]
years.extend([2021])
tiers=[]
tiers.extend(data['tier'].unique())

tab_risk, tab_reg, tab_rep, tab_prod, tab_sup, tab_notes  = st.tabs(["Risk Overview", "Regulatory Risk", "Reputational Risk","Details - Products","Details - Suppliers","Notes"])

sb = st.sidebar.title('Assent Supply Chain Analysis')


with sb:
       
    risk_choices=st.sidebar.multiselect('risks to consider',risks)
    year_choice=st.sidebar.multiselect('year',years,default=max(years))
    supplier_choices=st.sidebar.multiselect('supplier',suppliers)
    tier_choices=st.sidebar.multiselect('tier',tiers, default=1)
    product_choices=st.sidebar.multiselect('product',products,default=products[0])
    
    
    
    select_data = scd.apply_rf(data.query("year=="+str(year_choice)+" and tier in ("+str(tier_choices)+")"))

    
with tab_risk:

    risk_c1 = st.container()
    risk_c2 = st.container()
    risk_c3 = st.container()
    
    with risk_c1:

        st.subheader("Overall Risk Rating and Y/Y change")
        
        risk_c1_col1,risk_c1_col2,risk_c1_col3 = st.columns(3)
        
        #st.plotly_chart(scf.risk_dash_fig(data_risk_sum),use_container_width=True)
        #st.plotly_chart(scf.risk_ESG_fig(),use_container_width=True)
        with risk_c1_col1:
            st.metric('Overall',71,delta=-5)
            
        with risk_c1_col2:
            st.metric('Regulatory Compliance',50,delta=10)
            
        with risk_c1_col3:
            st.metric('Reputational',62,delta=-12)
    
    with risk_c2:
    
        risk_c2_col1,risk_c2_col2 = st.columns(2)
    
        with risk_c2_col1:
            st.subheader("Regulatory risk breakdown")
            st.plotly_chart(scf.risk_reg_sum_fig(),use_container_width=True)
        
        with risk_c2_col2:
            st.subheader("Reputational risk breakdown")
            st.plotly_chart(scf.risk_rep_sum_fig(),use_container_width=True)
    

    with risk_c3:
    
        risk_c3_col1,risk_c3_col2,risk_c3_col3 = st.columns(3)
    
        with risk_c3_col1:
            st.subheader("Top product groups at risk")
            st.plotly_chart(scf.risk_prod_sum_fig(),use_container_width=True)
            #st.bar_chart(np.random.randn(5, 2))
            
        with risk_c3_col2:
            st.subheader("Top suppliers at risk")
            #st.plotly_chart(scf.risk_sup_sum_fig(),use_container_width=True)
            st.plotly_chart(scf.risk_prod_sum_fig(),use_container_width=True)
        
        with risk_c3_col3:
            st.subheader("Top supply regions at risk")
            #st.plotly_chart(scf.risk_sup_sum_fig(),use_container_width=True)
            st.plotly_chart(scf.risk_cat_region_fig(),use_container_width=True)
            
with tab_reg:
    reg_c1 = st.container()
    reg_c2 = st.container()
    
    with reg_c1:

        st.subheader("Regulatory Risk Overview")
        
        with st.expander("Regulatory Risk Details"):
            st.dataframe(data)
               
    with reg_c2:
        
        reg_col1,reg_col2,reg_col3 = st.columns(3)
    
        with reg_col1:
            st.subheader("Reg Risk breakdown 1")
        
        with reg_col2:
            st.subheader("Reg Risk breakdown 2")
    
        with reg_col3:
            st.subheader("Reg Risk breakdown 3")
            
with tab_rep:
    rep_c1 = st.container()
    rep_c2 = st.container()
    
    with rep_c1:

        
        st.subheader("Reputational Risk Overview")
        
        with st.expander("Reputational Risk Details"):
            st.dataframe(data)
               
    with rep_c2:
        
        rep_col1,rep_col2,rep_col3 = st.columns(3)
    
        with rep_col1:
            st.subheader("Rep Risk breakdown 1")
        
        with rep_col2:
            st.subheader("Rep Risk breakdown 2")
    
        with rep_col3:
            st.subheader("Rep Risk breakdown 3")

with tab_prod:
    prod_c1 = st.container()
    prod_c2 = st.container()
    
    with prod_c1:

        st.subheader("Product value chains")
        #select_data = scd.apply_rf(data.query("year=="+str(year_choice)+" and product in ("+str(product_choices)+")"))
        #dataset = scd.get_vc_data(select_data)
        #st.dataframe(dataset)
        #st.text(labels)
        #st.text(dataset['product_code'].values)
        
        st.plotly_chart(scf.prod_vc_fig(labels,select_data),use_container_width=True)
        
        with st.expander("Part Details"):
            st.dataframe(select_data[['year','tier','product','part','supplier','qty','e-climate_impact','e-biodiversity','s-human_trafficking','s-labor_rights','g-org_commitment','g-resiliency','total rating','total rating bin']])
            #st.dataframe(select_data)
               
    with prod_c2:
        
        prod_col1,prod_col2,prod_col3 = st.columns(3)
    
        with prod_col1:
            st.subheader("Product breakdown")
            #st.dataframe(scd.apply_rf(scd.rollup_to_prod(select_data)))
            st.plotly_chart(scf.horiz_bar_chart(scd.apply_rf(scd.rollup_to_prod(select_data))[['product','e-climate_impact','e-biodiversity','s-human_trafficking','s-labor_rights','g-org_commitment','g-resiliency','total rating']],'product'))
        
        with prod_col2:
            st.subheader("Supplier breakdown")
            st.plotly_chart(scf.horiz_bar_chart(scd.apply_rf(scd.rollup_to_sup(select_data))[['supplier','e-climate_impact','e-biodiversity','s-human_trafficking','s-labor_rights','g-org_commitment','g-resiliency','total rating']],'supplier'))
            
        with prod_col3:
            st.subheader("Country breakdown")
            st.plotly_chart(scf.horiz_bar_chart(scd.apply_rf(scd.rollup_to_country(select_data))[['country','e-climate_impact','e-biodiversity','s-human_trafficking','s-labor_rights','g-org_commitment','g-resiliency','total rating']],'country'))

with tab_sup:
    sup_c1 = st.container()
    sup_c2 = st.container()
    
    with sup_c1:

        st.subheader("Supplier Relationships")
        
        scf.supply_chain(nodes,links)
        HtmlFile = open("vc.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height = 600,width=2000)
    
        with st.expander("Supplier Details"):
            st.dataframe(select_data[['year','tier','product','part','supplier','qty','e-climate_impact','e-biodiversity','s-human_trafficking','s-labor_rights','g-org_commitment','g-resiliency','total rating','total rating bin']])              
    with sup_c2:
        
        sup_col1,sup_col2,sup_col3 = st.columns(3)
    
        with sup_col1:
            st.subheader("Supplier Risk breakdown 1")
        
        with sup_col2:
            st.subheader("Supplier Risk breakdown 2")
    
        with sup_col3:
            st.subheader("Supplier Risk breakdown 3")
with tab_notes:
        txt = st.text_area("To do:",notes, height=600)
        if st.button('Save'):
            scd.update_notes(txt)
            notes = txt
            st.success('changes saved to file')
