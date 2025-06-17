import streamlit as st
import json
import os
from datetime import datetime
from utils.progress_tracker import ProgressTracker

st.set_page_config(
    page_title="Planos de Aula - IA na Educação",
    page_icon="📝",
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

def load_lesson_templates():
    """Load lesson plan templates from JSON file"""
    try:
        with open('data/lesson_plans.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_lesson_plan(template, customizations):
    """Generate a customized lesson plan based on template and user inputs"""
    plan = template.copy()
    
    # Apply customizations
    plan['duration'] = customizations['duration']
    plan['grade_level'] = customizations['grade_level']
    plan['class_size'] = customizations['class_size']
    plan['focus_area'] = customizations['focus_area']
    
    # Adjust activities based on duration
    if customizations['duration'] <= 45:
        plan['activities'] = plan['activities'][:3]  # Shorter lesson
    elif customizations['duration'] >= 90:
        plan['activities'].extend([
            {
                "name": "Atividade Adicional - Debate Estendido",
                "duration": "20 min",
                "description": "Debate aprofundado sobre as implicações éticas dos vieses em IA"
            }
        ])
    
    return plan

def main():
    st.title("📝 Planos de Aula")
    st.markdown("Crie e personalize planos de aula sobre vieses em IA")
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Criar Plano", "📋 Modelos", "📚 Meus Planos"])
    
    with tab1:
        st.subheader("🎯 Gerador de Planos de Aula")
        
        # Load templates
        templates = load_lesson_templates()
        
        if not templates:
            st.error("Não foi possível carregar os modelos de planos de aula.")
            return
        
        # Template selection
        template_names = [template['title'] for template in templates]
        selected_template_name = st.selectbox(
            "Escolha um modelo base:",
            template_names,
            help="Selecione o modelo que melhor se adequa ao seu objetivo"
        )
        
        selected_template = next(t for t in templates if t['title'] == selected_template_name)
        
        # Display template preview
        with st.expander("👀 Visualizar Modelo"):
            st.markdown(f"**Objetivo:** {selected_template['objective']}")
            st.markdown(f"**Duração Sugerida:** {selected_template['suggested_duration']} minutos")
            st.markdown(f"**Nível:** {selected_template['target_grade']}")
            st.markdown(f"**Descrição:** {selected_template['description']}")
        
        # Customization form
        st.markdown("### ⚙️ Personalização")
        
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.slider(
                "Duração da aula (minutos):",
                30, 120, selected_template.get('suggested_duration', 60), 15
            )
            
            grade_level = st.selectbox(
                "Nível de ensino:",
                ["Ensino Fundamental I (1º-5º ano)", 
                 "Ensino Fundamental II (6º-9º ano)", 
                 "Ensino Médio", 
                 "Ensino Superior"]
            )
        
        with col2:
            class_size = st.number_input(
                "Tamanho da turma:",
                min_value=5, max_value=50, value=25, step=5
            )
            
            focus_area = st.selectbox(
                "Área de foco:",
                ["Identificação de Vieses", "Impactos Sociais", "Soluções Práticas", 
                 "Casos Reais", "Desenvolvimento Crítico"]
            )
        
        # Additional customizations
        st.markdown("### 🎨 Personalizações Adicionais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_technology = st.checkbox("Incluir atividades com tecnologia", value=True)
            include_discussion = st.checkbox("Incluir debates e discussões", value=True)
            include_practical = st.checkbox("Incluir exercícios práticos", value=True)
        
        with col2:
            difficulty_level = st.select_slider(
                "Nível de dificuldade:",
                ["Básico", "Intermediário", "Avançado"],
                value="Intermediário"
            )
            
            learning_style = st.multiselect(
                "Estilos de aprendizagem:",
                ["Visual", "Auditivo", "Cinestésico", "Leitura/Escrita"],
                default=["Visual", "Auditivo"]
            )
        
        # Generate lesson plan
        if st.button("🚀 Gerar Plano de Aula", use_container_width=True):
            customizations = {
                'duration': duration,
                'grade_level': grade_level,
                'class_size': class_size,
                'focus_area': focus_area,
                'include_technology': include_technology,
                'include_discussion': include_discussion,
                'include_practical': include_practical,
                'difficulty_level': difficulty_level,
                'learning_style': learning_style
            }
            
            generated_plan = generate_lesson_plan(selected_template, customizations)
            st.session_state.current_plan = generated_plan
            st.session_state.progress_tracker.update_progress('plans_created', 1)
            st.success("Plano de aula gerado com sucesso!")
            st.rerun()
    
    with tab2:
        st.subheader("📋 Modelos Disponíveis")
        
        templates = load_lesson_templates()
        
        for template in templates:
            with st.expander(f"📖 {template['title']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Objetivo:** {template['objective']}")
                    st.markdown(f"**Duração:** {template['suggested_duration']} min")
                    st.markdown(f"**Nível:** {template['target_grade']}")
                
                with col2:
                    st.markdown(f"**Materiais:** {', '.join(template['materials'])}")
                    st.markdown(f"**Competências:** {', '.join(template['skills'])}")
                
                st.markdown(f"**Descrição:** {template['description']}")
                
                # Activities preview
                if template.get('activities'):
                    st.markdown("**Atividades:**")
                    for activity in template['activities'][:3]:  # Show first 3 activities
                        st.markdown(f"• {activity['name']} ({activity['duration']})")
    
    with tab3:
        st.subheader("📚 Plano Gerado")
        
        if 'current_plan' in st.session_state:
            plan = st.session_state.current_plan
            
            # Plan header
            st.markdown(f"# {plan['title']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Duração", f"{plan['duration']} min")
            with col2:
                st.metric("Nível", plan['grade_level'])
            with col3:
                st.metric("Turma", f"{plan['class_size']} alunos")
            
            # Plan details
            st.markdown("## 🎯 Objetivo")
            st.markdown(plan['objective'])
            
            st.markdown("## 📝 Descrição")
            st.markdown(plan['description'])
            
            # Materials and skills
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("## 🛠️ Materiais Necessários")
                for material in plan['materials']:
                    st.markdown(f"• {material}")
            
            with col2:
                st.markdown("## 🎓 Competências Desenvolvidas")
                for skill in plan['skills']:
                    st.markdown(f"• {skill}")
            
            # Activities
            st.markdown("## 📋 Atividades")
            
            for i, activity in enumerate(plan['activities'], 1):
                with st.expander(f"Atividade {i}: {activity['name']} ({activity['duration']})"):
                    st.markdown(activity['description'])
                    
                    if activity.get('materials'):
                        st.markdown("**Materiais específicos:**")
                        for material in activity['materials']:
                            st.markdown(f"• {material}")
                    
                    if activity.get('instructions'):
                        st.markdown("**Instruções:**")
                        for instruction in activity['instructions']:
                            st.markdown(f"{instruction}")
            
            # Assessment
            if plan.get('assessment'):
                st.markdown("## 📊 Avaliação")
                st.markdown(plan['assessment'])
            
            # Export options
            st.markdown("---")
            st.markdown("## 📤 Exportar Plano")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📄 Exportar como Texto"):
                    # Generate text version
                    text_content = f"""
PLANO DE AULA: {plan['title']}

DURAÇÃO: {plan['duration']} minutos
NÍVEL: {plan['grade_level']}
TAMANHO DA TURMA: {plan['class_size']} alunos

OBJETIVO:
{plan['objective']}

DESCRIÇÃO:
{plan['description']}

MATERIAIS:
{chr(10).join(['• ' + material for material in plan['materials']])}

COMPETÊNCIAS:
{chr(10).join(['• ' + skill for skill in plan['skills']])}

ATIVIDADES:
{chr(10).join([f"{i+1}. {activity['name']} ({activity['duration']}) - {activity['description']}" for i, activity in enumerate(plan['activities'])])}
                    """
                    
                    st.download_button(
                        label="⬇️ Download TXT",
                        data=text_content,
                        file_name=f"plano_aula_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                if st.button("📋 Copiar para Área de Transferência"):
                    st.info("Funcionalidade em desenvolvimento")
            
            with col3:
                if st.button("📧 Compartilhar"):
                    st.info("Funcionalidade em desenvolvimento")
        
        else:
            st.info("Gere um plano de aula na aba 'Criar Plano' para visualizá-lo aqui.")
        
        # Progress display
        #progress = st.session_state.progress_tracker.get_progress()
        #st.markdown("---")
        #st.subheader("📈 Seu Progresso")
        #st.metric("Planos Criados", progress.get('plans_created', 0))

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
        st.page_link("pages/2_📚_Casos_Reais.py", label="📚 Casos Reais")
        st.page_link("pages/4_📖_Recursos.py", label="📖 Recursos")
        
        st.markdown("---")
        st.markdown("### 💡 Dicas")
        st.markdown("""
        - Adapte a linguagem ao nível dos alunos;
        - Inclua exemplos práticos e atuais;
        - Promova discussões e reflexões;
        - Use recursos visuais quando possível.
        """)

if __name__ == "__main__":
    main()
