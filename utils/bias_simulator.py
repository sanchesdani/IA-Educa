import random
import json
from typing import Dict, List, Any

class BiasSimulator:
    """Simulator for AI bias scenarios with interactive analysis"""
    
    def __init__(self):
        self.scenario_templates = self._load_scenario_templates()
        self.bias_types = {
            "Viés de Confirmação": "Tendência de buscar informações que confirmem crenças preexistentes",
            "Viés de Representação": "Dados de treinamento não representam adequadamente a população",
            "Viés de Seleção": "Distorções na forma como os dados foram coletados",
            "Viés Cultural": "Preconceitos baseados em normas culturais específicas",
            "Viés de Gênero": "Discriminação baseada em gênero",
            "Viés Racial": "Discriminação baseada em raça ou etnia",
            "Viés Socioeconômico": "Discriminação baseada em classe social"
        }
    
    def _load_scenario_templates(self) -> List[Dict]:
        """Load scenario templates from JSON file"""
        try:
            with open('data/bias_scenarios.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_scenarios()
    
    def _get_default_scenarios(self) -> List[Dict]:
        """Return default scenarios if file is not available"""
        return [
            {
                "type": "Seleção de Candidatos",
                "context": "Sistema de IA para triagem de currículos",
                "situation": "O sistema aprova mais candidatos homens que mulheres",
                "bias_type": "Viés de Gênero",
                "correct_identification": ["Viés de Gênero", "Viés de Representação"]
            }
        ]
    
    def generate_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """Generate a random scenario of the specified type"""
        # Filter scenarios by type
        matching_scenarios = [s for s in self.scenario_templates if s.get('type') == scenario_type]
        
        if not matching_scenarios:
            # Return a generic scenario if no match found
            return self._create_generic_scenario(scenario_type)
        
        # Select a random scenario
        base_scenario = random.choice(matching_scenarios)
        
        # Add some randomization to make it more interesting
        scenario = base_scenario.copy()
        scenario['id'] = random.randint(1000, 9999)
        
        return scenario
    
    def _create_generic_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """Create a generic scenario when specific type is not available"""
        generic_scenarios = {
            "Seleção de Candidatos": {
                "context": "Uma empresa usa IA para analisar currículos",
                "situation": "O sistema mostra padrões discriminatórios nas aprovações",
                "bias_type": "Viés de Representação"
            },
            "Reconhecimento Facial": {
                "context": "Sistema de reconhecimento facial em ambiente educacional",
                "situation": "O sistema tem dificuldade com certas características físicas",
                "bias_type": "Viés Racial"
            },
            "Recomendação de Conteúdo": {
                "context": "Plataforma educacional recomenda cursos",
                "situation": "As recomendações seguem padrões estereotípicos",
                "bias_type": "Viés de Gênero"
            },
            "Avaliação Automática": {
                "context": "Sistema de correção automática de textos",
                "situation": "Certas expressões culturais recebem notas menores",
                "bias_type": "Viés Cultural"
            },
            "Tradução Automática": {
                "context": "Sistema de tradução em escola internacional",
                "situation": "Profissões são traduzidas com estereótipos de gênero",
                "bias_type": "Viés de Gênero"
            }
        }
        
        template = generic_scenarios.get(scenario_type, {
            "context": "Sistema de IA em ambiente educacional",
            "situation": "O sistema apresenta comportamentos discriminatórios",
            "bias_type": "Viés de Representação"
        })
        
        return {
            "id": random.randint(1000, 9999),
            "type": scenario_type,
            "context": template["context"],
            "situation": template["situation"],
            "bias_type": template["bias_type"],
            "correct_identification": [template["bias_type"]]
        }
    
    def evaluate_response(self, scenario: Dict, bias_detected: str, bias_types: List[str], solution: str) -> Dict[str, Any]:
        """Evaluate user's response to a scenario"""
        score = 0
        feedback_parts = []
        
        # Check bias detection accuracy
        correct_bias_types = scenario.get('correct_identification', [scenario.get('bias_type', '')])
        
        if bias_detected in ["Sim, há viés evidente", "Possivelmente há viés"]:
            score += 30
            feedback_parts.append("✅ Identificou corretamente a presença de viés")
        else:
            feedback_parts.append("❌ Não identificou a presença de viés no cenário")
        
        # Check bias type identification
        if bias_types:
            matching_types = set(bias_types) & set(correct_bias_types)
            if matching_types:
                score += 40
                feedback_parts.append(f"✅ Identificou corretamente: {', '.join(matching_types)}")
            else:
                feedback_parts.append("⚠️ Tipos de viés identificados não correspondem ao cenário")
        
        # Evaluate solution quality
        if solution and len(solution.strip()) > 20:
            score += 30
            if any(keyword in solution.lower() for keyword in ['dados', 'treinamento', 'diversidade', 'teste', 'monitorar']):
                feedback_parts.append("✅ Proposta de solução inclui elementos técnicos relevantes")
            else:
                feedback_parts.append("⚠️ Solução pode ser mais específica em termos técnicos")
        else:
            feedback_parts.append("❌ Solução precisa ser mais detalhada")
        
        # Generate overall feedback
        if score >= 80:
            level = "Especialista"
            general_feedback = "Excelente análise! Você demonstra compreensão profunda sobre vieses em IA."
        elif score >= 60:
            level = "Intermediário"
            general_feedback = "Boa análise! Continue desenvolvendo suas habilidades de identificação de vieses."
        else:
            level = "Iniciante"
            general_feedback = "Continue praticando! A identificação de vieses requer experiência."
        
        # Generate recommendations
        recommendations = self._generate_recommendations(score, bias_types, correct_bias_types)
        
        return {
            "score": score,
            "accuracy": min(100, score + random.randint(-5, 15)),
            "level": level,
            "feedback": general_feedback,
            "detailed_feedback": feedback_parts,
            "explanation": self._generate_explanation(scenario),
            "recommendations": recommendations
        }
    
    def _generate_explanation(self, scenario: Dict) -> str:
        """Generate detailed explanation for the scenario"""
        bias_type = scenario.get('bias_type', 'Viés não especificado')
        explanation = f"""
        **Análise do Cenário:**
        
        Este cenário apresenta um caso de **{bias_type}**. 
        
        **Por que isso é um problema?**
        {self.bias_types.get(bias_type, 'Tipo de viés que pode causar discriminação injusta.')}
        
        **Como identificar:**
        - Analise se há disparidades nos resultados entre diferentes grupos
        - Verifique se os dados de treinamento são representativos
        - Considere o contexto histórico e social do problema
        
        **Impacto potencial:**
        Vieses como este podem perpetuar desigualdades, limitar oportunidades e afetar negativamente grupos já marginalizados.
        """
        
        return explanation
    
    def _generate_recommendations(self, score: int, identified_types: List[str], correct_types: List[str]) -> List[str]:
        """Generate personalized recommendations based on performance"""
        recommendations = []
        
        if score < 60:
            recommendations.extend([
                "Estude os diferentes tipos de vieses em IA e suas características",
                "Pratique com mais cenários para desenvolver intuição",
                "Foque em entender como dados de treinamento afetam os resultados"
            ])
        
        if not any(t in identified_types for t in correct_types):
            recommendations.append("Revise os tipos de vieses e suas definições")
        
        if score >= 60:
            recommendations.extend([
                "Explore estudos de caso reais para aprofundar conhecimento",
                "Considere aprender sobre métricas de equidade em ML",
                "Participe de discussões sobre IA ética"
            ])
        
        return recommendations
    
    def get_bias_info(self) -> Dict[str, str]:
        """Return information about different types of biases"""
        return self.bias_types
    
    def get_scenario_statistics(self) -> Dict[str, Any]:
        """Return statistics about available scenarios"""
        types = [s.get('type', 'Não especificado') for s in self.scenario_templates]
        
        return {
            "total_scenarios": len(self.scenario_templates),
            "types_available": list(set(types)),
            "most_common_type": max(set(types), key=types.count) if types else "N/A"
        }
