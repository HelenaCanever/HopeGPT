import streamlit as st
from functions import styling


styling.local_css('homepage_style.css')

st.image("images/logotype-default.png")
st.markdown("<h1 style='color:#FF5925'> Demo </h1>""", unsafe_allow_html=True)
st.markdown("<h4 style='color:#FF5925'> Utiliser les LLMs pour simuler l'empreinte carbone des missions Talan </h4>""", unsafe_allow_html=True)

st.markdown("Téléchargez votre réponse à un appel d'offres. Notre IA analysera le fichier pour rechercher toutes les informations dont elle a besoin. Une fois cela fait, elle vous fournira une estimation de l'empreinte carbone de la mission.")

st.markdown("<h4>"+styling.img_to_html(r"images/one.png") +" Téléchargez votre réponse à un appel d'offres en format Powerpoint</h4>", unsafe_allow_html=True)
st.markdown("<h4>"+styling.img_to_html(r"images/two.png") +" Vérifiez les informations extraites</h4>", unsafe_allow_html=True)
st.markdown("<h4>"+styling.img_to_html(r"images/three.png") +" Consultez la simulation</h4>", unsafe_allow_html=True)
st.markdown("<h4>"+styling.img_to_html(r"images/four.png") +" Téléchargez la simulation en format pdf</h4>", unsafe_allow_html=True)



uploaded_file = st.file_uploader("Télécharger un fichier Powerpoint", type=['ppt', 'pptx'])

