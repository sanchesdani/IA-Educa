import streamlit as st
import json
import random
from utils.bias_simulator import BiasSimulator
from utils.progress_tracker import ProgressTracker

st.set_page_config(
    page_title="Simulador de Vieses - IA na Educação",
    page_icon="🎯",
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

# Initialize components
if 'bias_simulator' not in st.session_state:
    st.session_state.bias_simulator = BiasSimulator()

if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()

def main():
    st.title("🎯 Simulador de Vieses em IA")
    st.markdown("Experimente cenários interativos para identificar diferentes tipos de vieses")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["🎮 Simulação Interativa", "📈 Resultados", "🎓 Aprendizado"])
    
    with tab1:
        st.subheader("Cenário de Simulação")
        
        # Scenario selection
        scenario_type = st.selectbox(
            "Escolha o tipo de cenário:",
            ["Seleção de Candidatos", "Reconhecimento Facial", "Recomendação de Conteúdo", 
             "Avaliação Automática", "Tradução Automática"],
            help="Cada cenário apresenta diferentes desafios relacionados a vieses"
        )
        
        if st.button("🎲 Gerar Novo Cenário", use_container_width=True):
            scenario = st.session_state.bias_simulator.generate_scenario(scenario_type)
            st.session_state.current_scenario = scenario
            st.rerun()
        
        if 'current_scenario' in st.session_state:
            scenario = st.session_state.current_scenario
            
            # Display scenario
            st.info(f"**Contexto:** {scenario['context']}")
            st.warning(f"**Situação:** {scenario['situation']}")
            
            # Interactive questions
            st.subheader("🤔 Análise do Cenário")
            
            col1, col2 = st.columns(2)
            
            with col1:
                bias_detected = st.radio(
                    "Você identifica algum viés neste cenário?",
                    ["Sim, há viés evidente", "Possivelmente há viés", "Não há viés", "Não tenho certeza"],
                    key="bias_detection"
                )
                
                if bias_detected in ["Sim, há viés evidente", "Possivelmente há viés"]:
                    bias_type = st.multiselect(
                        "Que tipo(s) de viés você identifica?",
                        ["Viés de Confirmação", "Viés de Representação", "Viés de Seleção", 
                         "Viés Cultural", "Viés de Gênero", "Viés Racial", "Viés Socioeconômico"],
                        key="bias_types"
                    )
            
            with col2:
                confidence = st.slider(
                    "Qual seu nível de confiança na análise?",
                    0, 100, 50,
                    help="0 = Muito incerto, 100 = Muito confiante"
                )
                
                solution = st.text_area(
                    "Como você abordaria este problema?",
                    placeholder="Descreva sua proposta de solução...",
                    key="solution_input"
                )
            
            if st.button("📝 Submeter Análise", use_container_width=True):
                # Process analysis
                feedback = st.session_state.bias_simulator.evaluate_response(
                    scenario, bias_detected, st.session_state.get('bias_types', []), solution
                )
                
                st.session_state.current_feedback = feedback
                st.session_state.progress_tracker.update_progress('simulations_completed', 1)
                st.success("Análise submetida! Veja o feedback na aba 'Resultados'")
                st.rerun()
    
    with tab2:
        st.subheader("📊 Feedback e Resultados")
        
        if 'current_feedback' in st.session_state:
            feedback = st.session_state.current_feedback
            
            # Score display
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pontuação", f"{feedback['score']}/100")
            with col2:
                st.metric("Acurácia", f"{feedback['accuracy']}%")
            with col3:
                st.metric("Nível", feedback['level'])
            
            # Detailed feedback
            if feedback['score'] >= 80:
                st.success("🎉 Excelente análise!")
            elif feedback['score'] >= 60:
                st.info("👍 Boa análise!")
            else:
                st.warning("💡 Continue praticando!")
            
            st.markdown(f"**Feedback:** {feedback['feedback']}")
            
            # Explanation
            with st.expander("📚 Explicação Detalhada"):
                st.markdown(feedback['explanation'])
            
            # Recommendations
            if feedback.get('recommendations'):
                with st.expander("💡 Recomendações"):
                    for rec in feedback['recommendations']:
                        st.markdown(f"• {rec}")
        
        else:
            st.info("Complete uma simulação para ver os resultados aqui.")
    
    with tab3:
        st.subheader("🎓 Conceitos e Aprendizado")
        
        # Bias types explanation
        with st.expander("📖 Tipos de Vieses em IA"):
            bias_info = {
                "Viés de Confirmação": "Tendência de buscar ou interpretar informações que confirmam crenças preexistentes",
                "Viés de Representação": "Quando os dados de treinamento não representam adequadamente a população real",
                "Viés de Seleção": "Distorções causadas pela forma como os dados foram coletados ou selecionados",
                "Viés Cultural": "Preconceitos baseados em normas e valores culturais específicos",
                "Viés de Gênero": "Discriminação baseada em gênero presente nos dados ou algoritmos",
                "Viés Racial": "Discriminação baseada em raça ou etnia",
                "Viés Socioeconômico": "Discriminação baseada em classe social ou status econômico"
            }
            
            for bias_type, description in bias_info.items():
                st.markdown(f"**{bias_type}:** {description}")
        
        # Learning resources
        with st.expander("📚 Recursos de Aprendizado"):
            st.markdown("""
            ### Como Identificar Vieses:
            1. **Analise os dados de entrada** - Os dados são representativos?
            2. **Examine os resultados** - Há padrões discriminatórios?
            3. **Considere o contexto** - Quais grupos podem ser afetados?
            4. **Teste com cenários diversos** - Como o sistema responde a diferentes inputs?
            5. **Busque perspectivas múltiplas** - Envolva diferentes pontos de vista
            
            ### Estratégias de Mitigação:
            - Diversificar equipes de desenvolvimento
            - Usar dados balanceados e representativos
            - Implementar testes de equidade
            - Monitorar continuamente os resultados
            - Estabelecer mecanismos de feedback
            """)
        
        # Progress tracking
        progress = st.session_state.progress_tracker.get_progress()
        st.markdown("---")
        st.subheader("📈 Seu Progresso no Simulador")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Simulações Completadas", progress.get('simulations_completed', 0))
        with col2:
            if progress.get('simulations_completed', 0) > 0:
                avg_score = progress.get('total_score', 0) / progress.get('simulations_completed', 1)
                st.metric("Pontuação Média", f"{avg_score:.1f}")
                
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
        st.page_link("pages/2_📚_Casos_Reais.py", label="📚 Casos Reais")
        st.page_link("pages/3_📝_Planos_de_Aula.py", label="📝 Planos de Aula")
        st.page_link("pages/4_📖_Recursos.py", label="📖 Recursos")

if __name__ == "__main__":
    main()
