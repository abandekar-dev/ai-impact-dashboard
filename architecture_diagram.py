import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Create a comprehensive architecture diagram for the AI Strategic Modeling Platform"""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors
    colors = {
        'frontend': '#4A90E2',
        'backend': '#7ED321', 
        'database': '#F5A623',
        'ai_services': '#9013FE',
        'analytics': '#FF6B6B',
        'integration': '#50E3C2'
    }
    
    # Title
    ax.text(8, 11.5, 'AI-Powered Strategic Modeling Platform Architecture', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Frontend Layer
    frontend_box = FancyBboxPatch((0.5, 9), 15, 1.5, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor=colors['frontend'], 
                                 alpha=0.7, 
                                 edgecolor='black')
    ax.add_patch(frontend_box)
    ax.text(8, 9.75, 'Frontend Layer - Streamlit Interactive Dashboard', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Frontend components
    frontend_components = [
        ('Enhanced Function\nAnalysis', 1.5, 8.3),
        ('Monte Carlo\nSimulation', 3.5, 8.3),
        ('AI Workflow\nIntegration', 5.5, 8.3),
        ('Workforce\nAnalytics', 7.5, 8.3),
        ('Performance\nAnalysis', 9.5, 8.3),
        ('Learning\nPersonas', 11.5, 8.3),
        ('AI Assistant\nChat', 13.5, 8.3),
        ('Executive\nSummary', 14.5, 8.3)
    ]
    
    for comp, x, y in frontend_components:
        comp_box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                                 boxstyle="round,pad=0.05",
                                 facecolor='lightblue',
                                 edgecolor='navy',
                                 alpha=0.8)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Business Logic Layer
    logic_box = FancyBboxPatch((0.5, 6.5), 15, 1.2,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['backend'],
                              alpha=0.7,
                              edgecolor='black')
    ax.add_patch(logic_box)
    ax.text(8, 7.1, 'Business Logic & Processing Layer', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Business logic components
    logic_components = [
        ('Category\nManager', 2, 6.2),
        ('Predictive\nEngine', 4, 6.2),
        ('Session\nManager', 6, 6.2),
        ('Natural Language\nProcessor', 8, 6.2),
        ('Cross-Function\nAnalyzer', 10, 6.2),
        ('Benchmarking\nUtils', 12, 6.2),
        ('Vector\nDatabase', 14, 6.2)
    ]
    
    for comp, x, y in logic_components:
        comp_box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5,
                                 boxstyle="round,pad=0.05",
                                 facecolor='lightgreen',
                                 edgecolor='darkgreen',
                                 alpha=0.8)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # AI Services Layer
    ai_box = FancyBboxPatch((0.5, 4.8), 15, 1.2,
                           boxstyle="round,pad=0.1",
                           facecolor=colors['ai_services'],
                           alpha=0.7,
                           edgecolor='black')
    ax.add_patch(ai_box)
    ax.text(8, 5.4, 'AI Services & Analytics Layer', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # AI services components
    ai_components = [
        ('OpenAI\nIntegration', 2, 4.5),
        ('Predictive\nModeling', 4, 4.5),
        ('Semantic\nAnalyzer', 6, 4.5),
        ('Monte Carlo\nSimulator', 8, 4.5),
        ('Industry\nBenchmarking', 10, 4.5),
        ('Workforce\nPredictor', 12, 4.5),
        ('ROI\nCalculator', 14, 4.5)
    ]
    
    for comp, x, y in ai_components:
        comp_box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5,
                                 boxstyle="round,pad=0.05",
                                 facecolor='lavender',
                                 edgecolor='purple',
                                 alpha=0.8)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Data Layer
    data_box = FancyBboxPatch((0.5, 3.1), 15, 1.2,
                             boxstyle="round,pad=0.1",
                             facecolor=colors['database'],
                             alpha=0.7,
                             edgecolor='black')
    ax.add_patch(data_box)
    ax.text(8, 3.7, 'Data Storage & Management Layer', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # Data components
    data_components = [
        ('PostgreSQL\nDatabase', 3, 3.4),
        ('pgvector\nExtension', 5, 3.4),
        ('Session\nState', 7, 3.4),
        ('Local\nStorage', 9, 3.4),
        ('Enterprise\nIntegrations', 11, 3.4),
        ('Data\nValidation', 13, 3.4)
    ]
    
    for comp, x, y in data_components:
        comp_box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5,
                                 boxstyle="round,pad=0.05",
                                 facecolor='wheat',
                                 edgecolor='orange',
                                 alpha=0.8)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # External Integrations
    ext_box = FancyBboxPatch((0.5, 1.4), 15, 1.2,
                            boxstyle="round,pad=0.1",
                            facecolor=colors['integration'],
                            alpha=0.7,
                            edgecolor='black')
    ax.add_patch(ext_box)
    ax.text(8, 2, 'External Integrations & APIs', 
            ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    # External integration components
    ext_components = [
        ('ERP\nSystems', 2.5, 1.7),
        ('HRM\nPlatforms', 4.5, 1.7),
        ('OpenAI\nAPI', 6.5, 1.7),
        ('Industry\nDatabases', 8.5, 1.7),
        ('Cloud\nServices', 10.5, 1.7),
        ('Enterprise\nSecurity', 12.5, 1.7)
    ]
    
    for comp, x, y in ext_components:
        comp_box = FancyBboxPatch((x-0.6, y-0.25), 1.2, 0.5,
                                 boxstyle="round,pad=0.05",
                                 facecolor='lightcyan',
                                 edgecolor='teal',
                                 alpha=0.8)
        ax.add_patch(comp_box)
        ax.text(x, y, comp, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # Add data flow arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='gray', alpha=0.7)
    
    # Frontend to Business Logic
    ax.annotate('', xy=(8, 6.5), xytext=(8, 8.2), arrowprops=arrow_props)
    
    # Business Logic to AI Services
    ax.annotate('', xy=(8, 4.8), xytext=(8, 6.5), arrowprops=arrow_props)
    
    # AI Services to Data Layer
    ax.annotate('', xy=(8, 3.1), xytext=(8, 4.8), arrowprops=arrow_props)
    
    # Data Layer to External Integrations
    ax.annotate('', xy=(8, 1.4), xytext=(8, 3.1), arrowprops=arrow_props)
    
    # Add side arrows for data flow
    # Natural Language Processor to OpenAI
    ax.annotate('', xy=(6.5, 2.6), xytext=(8, 4.2), 
                arrowprops=dict(arrowstyle='->', lw=1.5, color='purple', alpha=0.7))
    
    # Vector Database to pgvector
    ax.annotate('', xy=(5, 3.9), xytext=(14, 5.9), 
                arrowprops=dict(arrowstyle='->', lw=1.5, color='blue', alpha=0.7))
    
    # Add Phase 1 Enhancement Box
    phase1_box = FancyBboxPatch((12.5, 0.2), 3, 1,
                               boxstyle="round,pad=0.1",
                               facecolor='gold',
                               alpha=0.8,
                               edgecolor='darkorange')
    ax.add_patch(phase1_box)
    ax.text(14, 0.7, 'Phase 1 Enhancements:\n• Natural Language Config\n• Cross-Function Analysis\n• Vector Database\n• Industry Intelligence', 
            ha='center', va='center', fontsize=9, fontweight='bold')
    
    # Add legend
    legend_elements = [
        ('Frontend', colors['frontend']),
        ('Business Logic', colors['backend']),
        ('AI Services', colors['ai_services']),
        ('Data Storage', colors['database']),
        ('External APIs', colors['integration'])
    ]
    
    for i, (label, color) in enumerate(legend_elements):
        legend_box = FancyBboxPatch((0.5, 0.8 - i*0.15), 0.3, 0.1,
                                   boxstyle="round,pad=0.02",
                                   facecolor=color,
                                   alpha=0.7)
        ax.add_patch(legend_box)
        ax.text(0.9, 0.85 - i*0.15, label, ha='left', va='center', fontsize=9)
    
    ax.text(0.65, 1.05, 'Legend:', ha='center', va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Create and save the architecture diagram
    fig = create_architecture_diagram()
    
    # Save as high-resolution PNG
    plt.savefig('ai_platform_architecture.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Save as SVG for scalability
    plt.savefig('ai_platform_architecture.svg', format='svg', bbox_inches='tight',
                facecolor='white', edgecolor='none')
    
    # Don't display interactively to avoid timeout
    # plt.show()
    
    print("Architecture diagram created successfully!")
    print("Files saved:")
    print("- ai_platform_architecture.png (high-resolution)")
    print("- ai_platform_architecture.svg (scalable vector)")