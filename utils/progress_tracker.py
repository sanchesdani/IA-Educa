import json
from typing import Dict, Any, List
from datetime import datetime

class ProgressTracker:
    """Track user progress across different activities in the platform"""
    
    def __init__(self):
        self.progress_data = {
            'simulations_completed': 0,
            'cases_studied': 0,
            'plans_created': 0,
            'resources_accessed': 0,
            'total_score': 0,
            'sessions': 0,
            'last_activity': None,
            'achievements': [],
            'activity_history': []
        }
        self.achievements = self._define_achievements()
    
    def _define_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Define available achievements and their criteria"""
        return {
            'first_simulation': {
                'name': '🎯 Primeiro Simulador',
                'description': 'Completou sua primeira simulação de viés',
                'criteria': lambda data: data['simulations_completed'] >= 1
            },
            'case_explorer': {
                'name': '📚 Explorador de Casos',
                'description': 'Estudou 5 casos reais de vieses em IA',
                'criteria': lambda data: data['cases_studied'] >= 5
            },
            'plan_creator': {
                'name': '📝 Criador de Planos',
                'description': 'Criou seu primeiro plano de aula',
                'criteria': lambda data: data['plans_created'] >= 1
            },
            'resource_hunter': {
                'name': '📖 Caçador de Recursos',
                'description': 'Acessou 10 recursos educacionais',
                'criteria': lambda data: data['resources_accessed'] >= 10
            },
            'bias_expert': {
                'name': '🏆 Especialista em Vieses',
                'description': 'Completou 10 simulações com pontuação média acima de 80',
                'criteria': lambda data: (data['simulations_completed'] >= 10 and 
                                        data['total_score'] / data['simulations_completed'] >= 80 
                                        if data['simulations_completed'] > 0 else False)
            },
            'educator': {
                'name': '🎓 Educador Consciente',
                'description': 'Criou 3 planos de aula e estudou 10 casos',
                'criteria': lambda data: data['plans_created'] >= 3 and data['cases_studied'] >= 10
            },
            'frequent_learner': {
                'name': '📅 Aprendiz Constante',
                'description': 'Realizou atividades em 7 sessões diferentes',
                'criteria': lambda data: data['sessions'] >= 7
            }
        }
    
    def update_progress(self, activity_type: str, value: int = 1, score: int = None) -> None:
        """Update progress for a specific activity"""
        if activity_type in self.progress_data:
            self.progress_data[activity_type] += value
        
        # Update score if provided
        if score is not None and activity_type == 'simulations_completed':
            self.progress_data['total_score'] += score
        
        # Update last activity timestamp
        self.progress_data['last_activity'] = datetime.now().isoformat()
        
        # Record activity in history
        self.progress_data['activity_history'].append({
            'type': activity_type,
            'value': value,
            'score': score,
            'timestamp': self.progress_data['last_activity']
        })
        
        # Check for new achievements
        self._check_achievements()
    
    def _check_achievements(self) -> None:
        """Check if user has earned any new achievements"""
        current_achievements = set(self.progress_data['achievements'])
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in current_achievements:
                if achievement['criteria'](self.progress_data):
                    self.progress_data['achievements'].append(achievement_id)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data"""
        return self.progress_data.copy()
    
    def get_achievements(self) -> List[Dict[str, Any]]:
        """Get list of earned achievements with details"""
        earned_achievements = []
        
        for achievement_id in self.progress_data['achievements']:
            if achievement_id in self.achievements:
                achievement = self.achievements[achievement_id].copy()
                achievement['id'] = achievement_id
                earned_achievements.append(achievement)
        
        return earned_achievements
    
    def get_next_achievements(self) -> List[Dict[str, Any]]:
        """Get list of next achievements user can earn"""
        current_achievements = set(self.progress_data['achievements'])
        next_achievements = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id not in current_achievements:
                progress_info = self._get_achievement_progress(achievement_id)
                achievement_info = achievement.copy()
                achievement_info['id'] = achievement_id
                achievement_info['progress'] = progress_info
                next_achievements.append(achievement_info)
        
        return next_achievements
    
    def _get_achievement_progress(self, achievement_id: str) -> Dict[str, Any]:
        """Calculate progress towards a specific achievement"""
        # This is a simplified version - in a real implementation,
        # you would analyze the criteria more sophisticatedly
        data = self.progress_data
        
        progress_info = {
            'first_simulation': {
                'current': data['simulations_completed'],
                'target': 1,
                'percentage': min(100, data['simulations_completed'] * 100)
            },
            'case_explorer': {
                'current': data['cases_studied'],
                'target': 5,
                'percentage': min(100, (data['cases_studied'] / 5) * 100)
            },
            'plan_creator': {
                'current': data['plans_created'],
                'target': 1,
                'percentage': min(100, data['plans_created'] * 100)
            },
            'resource_hunter': {
                'current': data['resources_accessed'],
                'target': 10,
                'percentage': min(100, (data['resources_accessed'] / 10) * 100)
            },
            'bias_expert': {
                'current': data['simulations_completed'],
                'target': 10,
                'percentage': min(100, (data['simulations_completed'] / 10) * 100)
            },
            'educator': {
                'current': min(data['plans_created'], data['cases_studied']),
                'target': min(3, 10),
                'percentage': min(100, (min(data['plans_created'] / 3, data['cases_studied'] / 10)) * 100)
            },
            'frequent_learner': {
                'current': data['sessions'],
                'target': 7,
                'percentage': min(100, (data['sessions'] / 7) * 100)
            }
        }
        
        return progress_info.get(achievement_id, {'current': 0, 'target': 1, 'percentage': 0})
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics for display"""
        data = self.progress_data
        
        # Calculate average score
        avg_score = (data['total_score'] / data['simulations_completed'] 
                    if data['simulations_completed'] > 0 else 0)
        
        # Calculate total activities
        total_activities = (data['simulations_completed'] + 
                          data['cases_studied'] + 
                          data['plans_created'] + 
                          data['resources_accessed'])
        
        # Determine user level
        level = self._calculate_user_level(total_activities, avg_score)
        
        return {
            'total_activities': total_activities,
            'average_score': round(avg_score, 1),
            'achievements_earned': len(data['achievements']),
            'user_level': level,
            'days_active': self._calculate_days_active(),
            'last_activity': data['last_activity']
        }
    
    def _calculate_user_level(self, total_activities: int, avg_score: float) -> str:
        """Calculate user level based on activities and performance"""
        if total_activities >= 50 and avg_score >= 80:
            return "Especialista"
        elif total_activities >= 25 and avg_score >= 70:
            return "Avançado"
        elif total_activities >= 10 and avg_score >= 60:
            return "Intermediário"
        elif total_activities >= 5:
            return "Iniciante"
        else:
            return "Novo"
    
    def _calculate_days_active(self) -> int:
        """Calculate number of different days user was active"""
        if not self.progress_data['activity_history']:
            return 0
        
        # Extract unique dates from activity history
        dates = set()
        for activity in self.progress_data['activity_history']:
            try:
                date = datetime.fromisoformat(activity['timestamp']).date()
                dates.add(date)
            except (ValueError, KeyError):
                continue
        
        return len(dates)
    
    def reset_progress(self) -> None:
        """Reset all progress data (use with caution)"""
        self.progress_data = {
            'simulations_completed': 0,
            'cases_studied': 0,
            'plans_created': 0,
            'resources_accessed': 0,
            'total_score': 0,
            'sessions': 0,
            'last_activity': None,
            'achievements': [],
            'activity_history': []
        }
    
    def export_progress(self) -> str:
        """Export progress data as JSON string"""
        return json.dumps(self.progress_data, indent=2, ensure_ascii=False)
    
    def import_progress(self, progress_json: str) -> bool:
        """Import progress data from JSON string"""
        try:
            imported_data = json.loads(progress_json)
            # Validate that all required keys exist
            required_keys = ['simulations_completed', 'cases_studied', 'plans_created', 
                           'resources_accessed', 'total_score', 'sessions']
            
            if all(key in imported_data for key in required_keys):
                self.progress_data.update(imported_data)
                return True
            else:
                return False
        except (json.JSONDecodeError, TypeError):
            return False
