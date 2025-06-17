import streamlit as st
import json
from utils.progress_tracker import ProgressTracker

st.set_page_config(
    page_title="Recursos - IA na Educação",
    page_icon="📖",
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

def main():
    st.title("📖 Recursos Educacionais")
    st.markdown("Materiais de apoio para aprofundar o conhecimento sobre vieses em IA")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Bibliografia", "🎥 Vídeos", "🔗 Links Úteis", "📊 Ferramentas para Utilização Pedagógica"])
    
    with tab1:
        st.subheader("📚 Bibliografia Recomendada")
        
        # Books and articles
        resources = [
            {
                "title": "Weapons of Math Destruction",
                "author": "Cathy O'Neil",
                "type": "Livro",
                "description": "Como algoritmos aumentam a desigualdade e ameaçam a democracia",
                "level": "Intermediário",
                "link": "https://www.amazon.com.br/dp/0553418815"
            },
            {
                "title": "Algorithms of Oppression",
                "author": "Safiya Umoja Noble",
                "type": "Livro",
                "description": "Como os mecanismos de busca reforçam o racismo",
                "level": "Avançado",
                "link": "https://nyupress.org/9781479837243/algorithms-of-oppression/"
            },
            {
                "title": "Race After Technology",
                "author": "Ruha Benjamin",
                "type": "Livro",
                "description": "Ferramentas abolitivas para a era digital",
                "level": "Intermediário",
                "link": "https://www.ruhabenjamin.com/race-after-technology"
            },
            {
                "title": "The Ethical Algorithm",
                "author": "Kearns & Roth",
                "type": "Livro",
                "description": "A ciência de design de algoritmo socialmente consciente",
                "level": "Avançado",
                "link": "https://global.oup.com/academic/product/the-ethical-algorithm-9780190948207"
            }
        ]
        
        for resource in resources:
            with st.expander(f"📖 {resource['title']} - {resource['author']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Tipo:** {resource['type']}")
                    st.markdown(f"**Nível:** {resource['level']}")
                    st.markdown(f"**Descrição:** {resource['description']}")
                
                with col2:
                    if st.button(f"🔗 Acessar", key=f"book_{resource['title']}"):
                        st.session_state.progress_tracker.update_progress('resources_accessed', 1)
                        st.success("Recurso acessado!")
        
        st.markdown("### 📑 Artigos Acadêmicos")
        
        articles = [
            {
                "title": "Fairness and Abstraction in Sociotechnical Systems",
                "authors": "Selbst et al.",
                "venue": "FAT* 2019",
                "description": "Análise dos desafios de implementar equidade em sistemas sociotécnicos"
            },
            {
                "title": "Gender Shades: Intersectional Accuracy Disparities",
                "authors": "Joy Buolamwini & Timnit Gebru",
                "venue": "FAT* 2018",
                "description": "Estudo sobre vieses em sistemas de reconhecimento facial"
            }
        ]
        
        for article in articles:
            st.markdown(f"**{article['title']}** ({article['venue']})")
            st.markdown(f"*{article['authors']}*")
            st.markdown(f"{article['description']}")
            st.markdown("---")
    
    with tab2:
        st.subheader("🎥 Vídeos Educacionais")
        
        videos = [
            {
                "title": "Como ensinar algoritmos a serem justos",
                "creator": "TED Talk - Joy Buolamwini",
                "duration": "9 min",
                "description": "Discussão sobre vieses em reconhecimento facial",
                "level": "Básico",
                "embed_id": "UG_X_7g63rY"
            },
            {
                "title": "Os perigos dos algoritmos invisíveis",
                "creator": "TED Talk - Cathy O'Neil",
                "duration": "13 min",
                "description": "Como algoritmos podem perpetuar desigualdades",
                "level": "Intermediário",
                "embed_id": "heQzqX35c9A"
            },
            {
                "title": "Inteligência Artificial e Preconceito",
                "creator": "Computerphile",
                "duration": "15 min",
                "description": "Explicação técnica sobre vieses em IA",
                "level": "Avançado",
                "embed_id": "59bMh59JQDo"
            }
        ]
        
        for video in videos:
            with st.expander(f"🎥 {video['title']} ({video['duration']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Criador:** {video['creator']}")
                    st.markdown(f"**Nível:** {video['level']}")
                    st.markdown(f"**Descrição:** {video['description']}")
                
                with col2:
                    if st.button(f"▶️ Assistir", key=f"video_{video['title']}"):
                        st.session_state.progress_tracker.update_progress('resources_accessed', 1)
                        st.info(f"Abrindo vídeo... [Link: https://youtube.com/watch?v={video['embed_id']}]")
    
    with tab3:
        st.subheader("🔗 Links Úteis")
        
        # Websites and tools
        links = [
            {
                "title": "AI Fairness 360",
                "url": "https://aif360.mybluemix.net/",
                "description": "Toolkit da IBM para detectar e mitigar vieses em ML",
                "category": "Ferramenta"
            },
            {
                "title": "Fairlearn",
                "url": "https://fairlearn.org/",
                "description": "Biblioteca Python para avaliação e melhoria de equidade",
                "category": "Ferramenta"
            },
            {
                "title": "Partnership on AI",
                "url": "https://partnershiponai.org/",
                "description": "Organização focada em IA responsável",
                "category": "Organização"
            },
            {
                "title": "AI Ethics Lab",
                "url": "https://aiethicslab.com/",
                "description": "Recursos sobre ética em inteligência artificial",
                "category": "Educacional"
            },
            {
                "title": "Algorithmic Justice League",
                "url": "https://www.ajl.org/",
                "description": "Organização combatendo vieses algorítmicos",
                "category": "Organização"
            }
        ]
        
        # Group by category
        categories = list(set([link['category'] for link in links]))
        
        for category in categories:
            st.markdown(f"### {category}")
            category_links = [link for link in links if link['category'] == category]
            
            for link in category_links:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{link['title']}**")
                    st.markdown(link['description'])
                
                with col2:
                    if st.button("🌐 Visitar", key=f"link_{link['title']}"):
                        st.session_state.progress_tracker.update_progress('resources_accessed', 1)
                        st.success("Link acessado!")
            
            st.markdown("---")
    
    with tab4:
        #st.subheader("📊 Ferramentas Interativas")
        
        st.markdown("## 🧮 Calculadora de Viés")
        
        st.markdown("Use esta ferramenta para analisar métricas de equidade em um dataset hipotético:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Grupo A (Maioria)")
            total_a = st.number_input("Total de casos - Grupo A", min_value=1, value=100, key="total_a")
            positive_a = st.number_input("Casos positivos - Grupo A", min_value=0, value=80, max_value=total_a, key="pos_a")
            predicted_positive_a = st.number_input("Predições positivas - Grupo A", min_value=0, value=75, max_value=total_a, key="pred_a")
        
        with col2:
            st.markdown("#### Grupo B (Minoria)")
            total_b = st.number_input("Total de casos - Grupo B", min_value=1, value=50, key="total_b")
            positive_b = st.number_input("Casos positivos - Grupo B", min_value=0, value=30, max_value=total_b, key="pos_b")
            predicted_positive_b = st.number_input("Predições positivas - Grupo B", min_value=0, value=20, max_value=total_b, key="pred_b")
        
        if st.button("📊 Calcular Métricas"):
            # Calculate metrics
            accuracy_a = predicted_positive_a / total_a if total_a > 0 else 0
            accuracy_b = predicted_positive_b / total_b if total_b > 0 else 0
            
            true_positive_rate_a = predicted_positive_a / positive_a if positive_a > 0 else 0
            true_positive_rate_b = predicted_positive_b / positive_b if positive_b > 0 else 0
            
            st.markdown("### 📈 Resultados")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Acurácia Grupo A", f"{accuracy_a:.2%}")
                st.metric("Acurácia Grupo B", f"{accuracy_b:.2%}")
                
                diff_accuracy = abs(accuracy_a - accuracy_b)
                st.metric("Diferença", f"{diff_accuracy:.2%}")
            
            with col2:
                st.metric("Taxa VP Grupo A", f"{true_positive_rate_a:.2%}")
                st.metric("Taxa VP Grupo B", f"{true_positive_rate_b:.2%}")
                
                diff_tpr = abs(true_positive_rate_a - true_positive_rate_b)
                st.metric("Diferença", f"{diff_tpr:.2%}")
            
            with col3:
                # Bias assessment
                if diff_accuracy > 0.1 or diff_tpr > 0.1:
                    st.error("⚠️ Possível viés detectado")
                elif diff_accuracy > 0.05 or diff_tpr > 0.05:
                    st.warning("⚡ Atenção necessária")
                else:
                    st.success("✅ Métricas equilibradas")
        
        st.markdown("## 🎯 Simulador de Decisões")
        
        st.markdown("Experimente como diferentes critérios afetam as decisões algorítmicas:")
        
        decision_criteria = st.multiselect(
            "Selecione os critérios de decisão:",
            ["Pontuação de Crédito", "Histórico Educacional", "Experiência Profissional", 
             "Localização", "Idade", "Gênero", "Referências"],
            default=["Pontuação de Crédito", "Histórico Educacional"]
        )
        
        bias_weight = st.slider(
            "Peso dos critérios potencialmente enviesados:",
            0.0, 1.0, 0.3, 0.1,
            help="Critérios como localização, idade e gênero podem introduzir vieses"
        )
        
        if st.button("🎲 Simular Decisões"):
            # Simple simulation
            import random
            
            results = []
            biased_criteria = ["Localização", "Idade", "Gênero"]
            
            for i in range(10):
                score = random.uniform(0.3, 0.9)
                
                # Apply bias if biased criteria are selected
                bias_applied = any(criterion in decision_criteria for criterion in biased_criteria)
                if bias_applied:
                    # Simulate bias effect
                    if random.random() < bias_weight:
                        score *= random.uniform(0.7, 1.3)  # Bias can help or hurt
                
                decision = "Aprovado" if score > 0.6 else "Rejeitado"
                results.append({"Caso": i+1, "Pontuação": f"{score:.2f}", "Decisão": decision})
            
            st.markdown("#### Resultados da Simulação")
            
            approved = len([r for r in results if r["Decisão"] == "Aprovado"])
            rejected = len([r for r in results if r["Decisão"] == "Rejeitado"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Aprovados", approved)
            with col2:
                st.metric("Rejeitados", rejected)
            
            # Show sample results
            st.markdown("**Amostra dos resultados:**")
            for result in results[:5]:
                st.markdown(f"Caso {result['Caso']}: {result['Pontuação']} → {result['Decisão']}")
    
    # Progress tracking
    #progress = st.session_state.progress_tracker.get_progress()
    #st.markdown("---")
    #st.subheader("📈 Recursos Acessados")
    #st.metric("Total", progress.get('resources_accessed', 0))

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
        st.page_link("pages/3_📝_Planos_de_Aula.py", label="📝 Planos de Aula")
        
        st.markdown("---")
        st.markdown("### 📊 Categoria de Recursos")
        st.markdown("• **Bibliografia:** Livros e artigos")
        st.markdown("• **Vídeos:** Conteúdo audiovisual")
        st.markdown("• **Links:** Sites e organizações")
        st.markdown("• **Ferramentas:** Recursos interativos")

if __name__ == "__main__":
    main()
