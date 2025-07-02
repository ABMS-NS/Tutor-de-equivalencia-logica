# tutor_logica.py - Controlador principal da aplicação

from src.config import setup_theme
from src.screens.main_window import MainWindow
from src.screens.levels_selection_window import LevelsSelectionWindow
from src.screens.exercise_window import ExerciseWindow

class TutorLogica:
    def __init__(self):
        # Configurar tema da aplicação
        setup_theme()
        
        # Janela principal (única janela inicial)
        self.main_window = MainWindow(self.handle_main_window_action)
        
        # Referências para outras janelas (controle de estado)
        self.levels_selection_window = None
        self.exercise_window = None
        
    def handle_main_window_action(self, action, *args):
        """
        Gerencia ações vindas da janela principal
        
        Ações possíveis:
        - "levels_selection": Abrir seleção de níveis (com perfil)
        """
        if action == "levels_selection":
            # Recebe perfil e perfil_path dos argumentos
            perfil = args[0] if len(args) > 0 else None
            perfil_path = args[1] if len(args) > 1 else None
            
            if perfil and perfil_path:
                self.abrir_levels_selection(perfil, perfil_path)
            else:
                print(" Erro: Perfil ou caminho não fornecidos")
    
    def abrir_levels_selection(self, perfil, perfil_path):
        """
        Abre a janela de seleção de níveis de exercícios
        
        Args:
            perfil (dict): Dados do perfil do usuário
            perfil_path (str): Caminho do arquivo do perfil
        """
    
        if hasattr(self, 'levels_selection_window') and self.levels_selection_window:
            try:
                if hasattr(self.levels_selection_window, 'window'):
                    self.levels_selection_window.window.destroy()
            except:
                pass
        
        
        self.levels_selection_window = LevelsSelectionWindow(
            parent=self.main_window.get_root(),
            app_instance=self,  
            perfil=perfil,
            perfil_path=perfil_path
        )
    
    def abrir_exercise_window(self, nivel, perfil_path):
        """
        Abre a janela de exercícios para o nível selecionado
        
        Args:
            nivel (int): Nível selecionado (1, 2, 3)
            perfil_path (str): Caminho do arquivo do perfil
        """
       
        if hasattr(self, 'exercise_window') and self.exercise_window:
            try:
                if hasattr(self.exercise_window, 'window'):
                    self.exercise_window.window.destroy()
            except:
                pass
        
        
        self.exercise_window = ExerciseWindow(
            parent=self.main_window.get_root(),
            nivel=nivel,
            app_instance=self,  
            perfil_path=perfil_path
        )
    
    def voltar_para_levels_selection(self, perfil, perfil_path):
        """
        Volta para a seleção de níveis (após completar exercício)
        
        Args:
            perfil (dict): Dados atualizados do perfil
            perfil_path (str): Caminho do arquivo do perfil
        """
       
        if hasattr(self, 'exercise_window') and self.exercise_window:
            try:
                if hasattr(self.exercise_window, 'window'):
                    self.exercise_window.window.destroy()
            except:
                pass
        
        if hasattr(self, 'levels_selection_window') and self.levels_selection_window:
            try:
                if hasattr(self.levels_selection_window, 'window'):
                    self.levels_selection_window.window.destroy()
            except:
                pass

     
        print(f" Voltando para levels_selection com perfil atualizado")
        self.abrir_levels_selection(perfil, perfil_path)
    
    def voltar_para_main_window(self):
        """Volta para a janela principal (menu inicial)"""
     
        if hasattr(self, 'levels_selection_window') and self.levels_selection_window:
            try:
                if hasattr(self.levels_selection_window, 'window'):
                    self.levels_selection_window.window.destroy()
            except:
                pass
                
        if hasattr(self, 'exercise_window') and self.exercise_window:
            try:
                if hasattr(self.exercise_window, 'window'):
                    self.exercise_window.window.destroy()
            except:
                pass
        
       
        try:
            root = self.main_window.get_root()
            root.deiconify()    
            root.lift()         
            root.focus_set()    
            print(" Voltou para main_window")
        except Exception as e:
            print(f" Erro ao voltar para main_window: {e}")
    
    def executar(self):
        """Inicia a aplicação"""
        try:
            self.main_window.executar()
        except Exception as e:
            print(f"Erro ao executar aplicação: {e}")

    def get_root(self):
        """Retorna a janela root principal (para casos especiais)"""
        return self.main_window.get_root()