# custom_button.py
import streamlit as st
import streamlit.components.v1 as components


def custom_button(label, key, on_click=None):
    button_id = f"button-{key}"
    custom_html = f"""
    <button id="{button_id}" style="
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        transition: all 0.3s ease;
    ">{label}</button>
    
    <script>
    const btn = document.getElementById('{button_id}');
    btn.onmouseover = function() {{
        this.style.backgroundColor = '#45a049';
        this.style.transform = 'scale(1.05)';
    }}
    btn.onmouseout = function() {{
        this.style.backgroundColor = '#4CAF50';
        this.style.transform = 'scale(1)';
    }}
    btn.onclick = function() {{
        this.style.backgroundColor = '#3e8e41';
        setTimeout(() => {{
            this.style.backgroundColor = '#4CAF50';
        }}, 200);
    }}
    </script>
    """

    clicked = components.html(custom_html, height=70)
    if clicked:
        on_click()
