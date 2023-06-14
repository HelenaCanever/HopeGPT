import streamlit as st
import base64
from pathlib import Path

import validators

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()} type='text/css'</style>", unsafe_allow_html=True)


def sidebar_hdr():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "HOPE";
                margin-left: 20px;
                margin-bottom: 20px;
                font-size: normal;
                font-weight: bold;
                position: relative;
                top: -50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def add_logo(logo_url: str, height: int = 120):
    """ Credits to: arnaudmiribe, streamlit-extras
    Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6
    The url can either be a url to the image, or a local path to the image.
    Args:
        logo_url (str): URL/local path of the logo
    """

    if validators.url(logo_url) is True:
        logo = f"url({logo_url})"
    else:
        logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-size: 250px;
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 40px 40px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=40' height='40'>".format(
    img_to_bytes(img_path)
    )
    return img_html

def logo_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width='600' >".format(
    img_to_bytes(img_path)
    )
    return img_html

def icon_to_html(img_path, size=25):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid' width=20' height='20'>".format(
    img_to_bytes(img_path)
    )
    return img_html