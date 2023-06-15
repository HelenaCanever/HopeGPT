import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import os
import json

#graph libraries

import plotly.express as px 
import plotly.io as pio
import plotly.graph_objects as go
from functions import styling, test_function

###styling settings
styling.local_css('homepage_style.css')
# Setting personalised graphs palette
palette = ['#60BCAC', '#3D00F2','#FF5925', '#98D7D9', '#76C3FF','#FEB29F','#C8E5E6','#CFEAFF','#FFE0D6',]
pio.templates["palette"] = go.layout.Template(
    layout = {
        'title':
            {'font': {'color': '#000000'}
            },
        'font': {'color': '#000000', 'family': 'Roboto'},
        'colorway': palette,
    }
)
pio.templates.default = "palette"


if "collaborators_output" not in st.session_state:
    st.session_state.collaborators_output = 0

if "months_output" not in st.session_state:
    st.session_state.months_output = 0

#intro
st.image("images/logotype-default.png")
st.markdown("<h1 style='color:#FF5925'> Demo </h1>""", unsafe_allow_html=True)
st.markdown("<h4 style='color:#FF5925'> Utiliser les LLMs pour simuler l'empreinte carbone des missions Talan </h4>""", unsafe_allow_html=True)

st.markdown("Téléchargez votre réponse à un appel d'offres. Notre IA analysera le fichier pour rechercher toutes les informations dont elle a besoin. Une fois cela fait, elle vous fournira une estimation de l'empreinte carbone de la mission.")

#upload powerpoint
st.markdown("<h4>"+styling.img_to_html(r"images/one.png") +" Téléchargez votre réponse à un appel d'offres en format Powerpoint</h4>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Télécharger un fichier Powerpoint", type=['ppt', 'pptx'])

#generate values
if uploaded_file and st.session_state.collaborators_output==0 and st.session_state.months_output==0:
    #substitute test_function.generate_output() with real LLM functions
    st.session_state.collaborators_output = test_function.generate_output()[0]
    st.session_state.months_output = test_function.generate_output()[1]

#human in the loop
if st.session_state.collaborators_output !=0 and st.session_state.months_output !=0:
    st.markdown("<h4>"+styling.img_to_html(r"images/two.png") +" Vérifiez les informations extraites</h4>", unsafe_allow_html=True)
    collaborators = st.number_input("Nombre de collaborateurs :", min_value=1, max_value=20, value=st.session_state.collaborators_output, help=None, on_change=None, args=None, label_visibility="visible")
    months = st.number_input("Durée de la mission en mois :", min_value=1, max_value=24, value=st.session_state.months_output, help=None, on_change=None, args=None, label_visibility="visible")

    #confirm output and display results
    if st.button("Je confirme"):    
        #standard emissions per consultant per month 
        emissions = {
            "plane":0,
            "tgv":0,
            "train":0,
            "ev":0,
            "car":0,
            "rer":3.49,
            "metro":0.55,
            "bus":0,
            "laptop":0.38,
            "phone":0.01,
            "email":0.20,
            "videoconference":0.14,
            "storage":0,
            "ml":0,
            "print":0.09
        }

        #calculate total emissions
        result= {}
        total_emissions = float(0)
        transport_emissions = float(0)
        digital_emissions = float(0)
        office_emissions = float(0) 

        for key, value in emissions.items():
            result[key] = round(value*collaborators*months, 2)
            total_emissions = round(total_emissions + result[key], 2)
            if key in ["plane","tgv","train","ev","car","rer","metro","bus"]:
                transport_emissions = round(transport_emissions + result[key], 2)
            elif key in ["laptop", "phone", "email", "videoconference", "storage", "ml"]:
                digital_emissions = round(digital_emissions + result[key], 2)
            else:
                office_emissions = round(office_emissions + result[key], 2)

        #display results
        st.markdown("<h4>"+styling.img_to_html(r"images/three.png") +" Consultez la simulation</h4>", unsafe_allow_html=True)

        st.metric("Émissions totales", "{} kgCO2eq".format(total_emissions))
        fig = px.pie(values=[
            transport_emissions, 
            digital_emissions, 
            office_emissions
            ], 
            names=["Déplacements", "Numérique", "Bureau"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
        fig.update_layout(legend=dict(x=0.85))
        fig.update_layout(
            font_color="black"
            )
        st.plotly_chart(fig, use_container_width=True)

        st.metric("Émissions liées aux déplacements", "{} kgCO2eq".format(transport_emissions))
        fig = px.pie(values=[
                result["plane"],
                result["tgv"],
                result["train"],
                result["ev"],
                result["car"],
                result["rer"],
                result["metro"],
                result["bus"]
                ], 
            names=["Avion", "TGV", "Train", "Voiture électrique", "Voiture thermique", "RER ou Transilien", "Metro", "Bus"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
        fig.update_layout(legend=dict(x=0.85))
        fig.update_layout(
            font_color="black"
            )
        st.plotly_chart(fig, use_container_width=True)
        #fig.write_image("./tmp/trasport_graph.png", engine="kaleido") 

        st.metric("Émissions liées au numérique", "{} kgCO2eq".format(digital_emissions)) 
        fig = px.pie(values=[
                result["laptop"],
                result["phone"],
                result["email"],
                result["videoconference"],
                result["storage"],
                result["ml"]
            ], 
            names=["Ordinateurs", "Smartphones", "Mails", "Visioconférences", "Stockage", "Machine Learning"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
        fig.update_layout(legend=dict(x=0.85))
        fig.update_layout(
            font_color="black"
            )
        st.plotly_chart(fig, use_container_width=True)
        #fig.write_image("./tmp/digital_graph.png", engine="kaleido") 

        st.metric("Émissions liées au aux activités de bureau", "{} kgCO2eq".format(office_emissions)) 
        fig = px.pie(values=[result["print"]], 
            names=["Impressions"])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
            })
        fig.update_layout(legend=dict(x=0.85))
        fig.update_layout(
            font_color="black"
            )
        st.plotly_chart(fig, use_container_width=True)
        #fig.write_image("./tmp/office_graph.png", engine="kaleido")      

        

        st.markdown("<h4>"+styling.img_to_html(r"images/four.png") +" Téléchargez la simulation en format pdf</h4>", unsafe_allow_html=True)
        st.write("Coming soon")
        #insert here code for conversion to pdf and download


