import streamlit as st
import json
import os
from utils.progress_tracker import ProgressTracker

st.set_page_config(
    page_title="Casos Reais - IA na Educação",
    page_icon="📚",
    layout="wide"
)
# Esconde a navegação automática do Streamlit
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Initialize progress tracker
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

def load_real_cases():
    """Load real cases from JSON file"""
    try:
        with open('data/real_cases.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    st.title("📚 Casos Reais de Vieses em IA")
    st.markdown("Explore exemplos concretos de como vieses aparecem em sistemas reais")
    
    cases = load_real_cases()
    
    if not cases:
        st.error("Não foi possível carregar os casos reais. Verifique se o arquivo de dados está disponível.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        category_filter = st.selectbox(
            "Filtrar por categoria:",
            ["Todos"] + list(set([case['category'] for case in cases]))
        )
    
    with col2:
        severity_filter = st.selectbox(
            "Filtrar por severidade:",
            ["Todos", "Baixa", "Média", "Alta"]
        )
    
    # Apply filters
    filtered_cases = cases
    if category_filter != "Todos":
        filtered_cases = [case for case in filtered_cases if case['category'] == category_filter]
    if severity_filter != "Todos":
        filtered_cases = [case for case in filtered_cases if case['severity'] == severity_filter]
    
    st.markdown(f"**{len(filtered_cases)}** casos encontrados")
    
    # Display cases
    for i, case in enumerate(filtered_cases):
        with st.expander(f"📖 {case['title']}", expanded=i==0):
            # Case header
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Categoria:** {case['category']}")
            with col2:
                severity_color = {"Baixa": "🟢", "Média": "🟡", "Alta": "🔴"}
                st.markdown(f"**Severidade:** {severity_color.get(case['severity'], '⚪')} {case['severity']}")
            with col3:
                st.markdown(f"**Ano:** {case['year']}")
            
            # Case content
            st.markdown("### 📝 Descrição do Caso")
            st.markdown(case['description'])
            
            st.markdown("### 🎯 Tipo de Viés Identificado")
            st.info(f"**{case['bias_type']}:** {case['bias_explanation']}")
            
            st.markdown("### ⚡ Impacto")
            st.warning(case['impact'])
            
            if case.get('solution'):
                st.markdown("### ✅ Solução Implementada")
                st.success(case['solution'])
            
            # Learning section
            st.markdown("### 🎓 Lições Aprendidas")
            for lesson in case['lessons']:
                st.markdown(f"• {lesson}")
            
            # Discussion questions
            if case.get('discussion_questions'):
                st.markdown("### 💭 Questões para Discussão")
                for question in case['discussion_questions']:
                    st.markdown(f"❓ {question}")
            
            # Interactive elements
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"📌 Marcar como Estudado", key=f"studied_{i}"):
                    st.session_state.progress_tracker.update_progress('cases_studied', 1)
                    st.success("Caso marcado como estudado!")
                    st.rerun()
            
            with col2:
                if st.button(f"📤 Compartilhar", key=f"share_{i}"):
                    st.info("Link copiado! [Funcionalidade em desenvolvimento]")
    
    # Summary section
    #if filtered_cases:
        #st.markdown("---")
        #st.subheader("📊 Resumo dos Casos")
        
        # Statistics
        #col1, col2, col3, col4 = st.columns(4)
        
        #categories = [case['category'] for case in filtered_cases]
        #severities = [case['severity'] for case in filtered_cases]
        #bias_types = [case['bias_type'] for case in filtered_cases]
        
        #with col1:
            #most_common_category = max(set(categories), key=categories.count)
            #st.metric("Categoria Mais Comum", most_common_category)
        
        #with col2:
            #most_common_severity = max(set(severities), key=severities.count)
            #st.metric("Severidade Mais Comum", most_common_severity)
        
        #with col3:
            #most_common_bias = max(set(bias_types), key=bias_types.count)
            #st.metric("Viés Mais Comum", most_common_bias)
        
        #with col4:
            #recent_cases = len([case for case in filtered_cases if case['year'] >= 2020])
            #st.metric("Casos Recentes (2020+)", recent_cases)
        
        # Key insights
        #st.markdown("### 💡 Principais Insights")
        
        #insights = [
            #"Vieses em IA são mais comuns em sistemas de reconhecimento e recomendação",
            #"A falta de diversidade nos dados de treinamento é uma causa frequente",
            #"Testes regulares e auditorias são essenciais para identificar problemas",
            #"A inclusão de equipes diversas no desenvolvimento reduz riscos",
            #"Transparência e explicabilidade ajudam na detecção precoce"
        #]
        
        #for insight in insights:
            #st.markdown(f"✅ {insight}")
    
    # Progress tracking
    #progress = st.session_state.progress_tracker.get_progress()
    #st.markdown("---")
    #st.subheader("📈 Seu Progresso")
    #st.metric("Casos Estudados", progress.get('cases_studied', 0))

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
        st.page_link("ia_edu.py", label="🏠 Página Inicial")
        st.page_link("pages/1_🎯_Simulador_de_Vieses.py", label="🎯 Simulador de Vieses")
        st.page_link("pages/3_📝_Planos_de_Aula.py", label="📝 Planos de Aula")
        st.page_link("pages/4_📖_Recursos.py", label="📖 Recursos")
        
        st.markdown("---")
        st.markdown("### 📊 Estatísticas")
        if cases:
            st.markdown(f"**Total de casos:** {len(cases)}")
            categories = list(set([case['category'] for case in cases]))
            st.markdown(f"**Categorias:** {len(categories)}")
            
            for category in categories:
                count = len([case for case in cases if case['category'] == category])
                st.markdown(f"• {category}: {count}")

if __name__ == "__main__":
    main()
