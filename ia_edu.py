import streamlit as st
import json
import os
from utils.progress_tracker import ProgressTracker

# Configure page
st.set_page_config(
    page_title="IA na Educação - Identificando Vieses em IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main { background-color: #f5f9fc; }
    .title { 
        color: #2c3e50; 
        text-align: center; 
        font-size: 2.8em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .header {
        color: #2980b9;
        border-bottom: 2px solid #3498db;
        padding-bottom: 10px;
    }
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 180px; /* Altura fixa para todos os cards */
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card h3 {
        margin-top: 0;
    }
    .card p {
        margin-bottom: 0;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .stButton>button {
        background-color: #bd3d3f;
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #674448;
        transform: scale(1.05);
    }
    .highlight {
        background-color: #efd7cf;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #deae9f;
        margin: 15px 0;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    .tab-content {
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize progress tracker
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

def main():
    # Header
    st.markdown('<div class="title">Identificando Vieses em IA</div>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="highlight">
    <b>Vieses em IA</b> são tendências indesejadas que sistemas de inteligência artificial podem aprender com dados humanos, 
    reforçando estereótipos e preconceitos. Esta ferramenta ajuda educadores a entender e ensinar sobre esse tema crucial.
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎯 Simulador de Vieses</h3>
            <p>Recursos para identificar vieses em ferramentas educacionais que você já usa</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Acessar Simulador", key="sim_btn", use_container_width=True):
            st.switch_page("pages/1_🎯_Simulador_de_Vieses.py")
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3>📚 Casos Reais</h3>
            <p>Exemplos concretos de como vieses aparecem na educação</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ver Casos Reais", key="cases_btn", use_container_width=True):
            st.switch_page("pages/2_📚_Casos_Reais.py")
    
    with col3:
        st.markdown("""
        <div class="card">
            <h3>📝 Planos de Aula</h3>
            <p>Atividades prontas para discutir ética em IA com seus alunos</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Criar Planos", key="plans_btn", use_container_width=True):
            st.switch_page("pages/3_📝_Planos_de_Aula.py")
    
    # How to use section (removida a seção de progresso)
    st.markdown("---")
    st.markdown("### 💡 Como usar esta ferramenta?")
    
    st.markdown("""
    1. Explore a seção **"O que são Vieses?"** para entender os conceitos básicos
    2. Analise **Casos Reais** de vieses em sistemas educacionais
    3. Experimente o **Simulador de Vieses** com seus alunos
    4. Adapte nossos **Planos de Aula** para sua realidade
    5. Compartilhe seus achados com outros educadores
    """)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <style>
            .sidebar-title {
                font-size: 1.5em;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
            }
            .sidebar-title i {
                margin-right: 10px;
            }
            /* Esconde a navegação automática do Streamlit */
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-title"><i>🧠</i> IA na Educação</div>', unsafe_allow_html=True)
        st.markdown("### Menu")
        
        # Lista de páginas simplificada
        st.page_link("ia_edu.py", label="🏠 Página Inicial")
        st.page_link("pages/1_🎯_Simulador_de_Vieses.py", label="🎯 Simulador de Vieses")
        st.page_link("pages/2_📚_Casos_Reais.py", label="📚 Casos Reais")
        st.page_link("pages/3_📝_Planos_de_Aula.py", label="📝 Planos de Aula")
        st.page_link("pages/4_📖_Recursos.py", label="📖 Recursos")
        
        st.markdown("---")
        st.markdown("## Plataforma voltada para a identificação e discussão de vieses em IA")
        st.markdown("""
        #### Autora: Danielle Sanches  
        <a href="https://www.linkedin.com/in/danielle-sanches-de-almeida-2a225a107/" target="_blank">LinkedIn</a> |
        <a href="http://lattes.cnpq.br/1290893382232095" target="_blank">Lattes</a>
        """, unsafe_allow_html=True)
        st.markdown("""
        #### Como citar a plataforma:
        Identificando Vieses em IA. Plataforma de Inteligência Artificial Aplicada à Educação Básica. Versão Atualizada, 2024. Disponível em: <a href= "https://aieduca.streamlit.app/" </a>. Acesso em:16 jun 2025.""")
        
        # Lista de páginas simplificada
        #st.page_link("ia_edu.py", label="🏠 Página Inicial")
        #st.page_link("pages/1_🎯_Simulador_de_Vieses.py", label="🎯 Simulador de Vieses")
        #st.page_link("pages/2_📚_Casos_Reais.py", label="📚 Casos Reais")
        #st.page_link("pages/3_📝_Planos_de_Aula.py", label="📝 Planos de Aula")
        #st.page_link("pages/4_📖_Recursos.py", label="📖 Recursos")
        
        #st.markdown("---")
        #st.markdown("## Plataforma voltada para a identificação e discussão de vieses em IA")
        #st.markdown("""
        #### Autora: Danielle Sanches  
        #<a href="https://www.linkedin.com/in/danielle-sanches-de-almeida-2a225a107/" target="_blank">LinkedIn</a> |
        #<a href="http://lattes.cnpq.br/1290893382232095" target="_blank">Lattes</a>
        #""", unsafe_allow_html=True)
        #st.markdown("""
        #### Como citar a plataforma:
        #Identificando Vieses em IA. Plataforma de Inteligência Artificial Aplicada à Educação Básica. Versão 2.0, 2024. Disponível em: https://aieduca.streamlit.app/. Acesso em: [DATA].""")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 3px;">
        <p>© 2025 Plataforma para Identificação de Vieses em Dados</p>
        <p>Plataforma Desenvolvida por educadores para educadores</p>
        <p style="font-size: small;">Versão 2.0 | Atualizado em Jun 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
