import seaborn as sns
import matplotlib.pyplot as plt
from app.config.settings import AppConfig

class BaseVisualizer:
    def __init__(self):
        self.config = AppConfig
        self.setup_style()
    
    def setup_style(self):
        sns.set_theme(style="whitegrid")
        plt.rcParams["figure.figsize"] = (
            self.config.PLOT_WIDTH,
            self.config.PLOT_HEIGHT
        )
    
    def create_figure(self):
        return plt.figure()