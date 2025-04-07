import streamlit as st

def show_sidebar():
    with st.sidebar:
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background-color: #0E1117;
                border-right: 1px solid rgba(49, 51, 63, 0.2);
            }

            /* Hide only the default navigation */
            section[data-testid="stSidebarNav"] {display: none !important;}
            div[data-testid="stSidebarNav"] {display: none !important;}
            
            /* Menu buttons styling */
            [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div > div > div > div > div > button {
                background-color: transparent !important;
                color: white !important;
                border: none !important;
                text-align: left !important;
                padding: 0.5rem 1rem !important;
                width: 100% !important;
                border-radius: 4px !important;
            }

            [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div > div > div > div > div > button:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }

            /* Logout button specific styling */
            [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:last-child button {
                background-color: #FF4B4B !important;
                color: white !important;
                border: none !important;
                text-align: left !important;
            }

            [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:last-child button:hover {
                background-color: #E43F3F !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # Menu items with icons
        menu_items = {
            "Dashboard": "📊",
            "Configurações": "⚙️",
            "Moedas Ativas": "💱",
            "Comprar Ordem": "💰",
            "Vender Ordem": "💸"
        }

        st.markdown("### Menu")
        selected = None

        # Create menu buttons
        for name, icon in menu_items.items():
            if st.button(f"{icon} {name}", use_container_width=True):
                selected = name.lower()

        # Add some space before the logout button
        st.markdown("<br>" * 10, unsafe_allow_html=True)

        # Logout button at the bottom
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['user_data'] = None
            st.switch_page("Home.py")

        # Navigation logic
        if selected:
            if selected == "dashboard":
                st.switch_page("pages/2_Dashboard.py")
            elif selected == "configurações":
                st.switch_page("pages/usuario_config.py")
            elif selected == "moedas ativas":
                st.switch_page("pages/moedas_ativas.py")
            elif selected == "comprar ordem":
                st.switch_page("pages/comprar_ordem.py")
            elif selected == "vender ordem":
                st.switch_page("pages/vender_ordem.py")

        return selected 