import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import numpy as np

# === Cargar datos ===
df = pd.read_excel(
    "Pivot.xlsx"
)

# --- Preprocesamiento ---
df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
df['valor'] = df['valor'].astype(str).str.replace(',', '.', regex=False)
df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
df['Año_Mes'] = df['Fecha'].dt.to_period('M').astype(str)

# Configuración de colores y tema
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#17becf',
    'accent': '#ff7f0e',
    'success': '#2ca02c',
    'info': '#17a2b8',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'water': '#0077be',
    'water_light': '#4da6d9',
    'water_dark': '#003d5c'
}

# App Dash
app = dash.Dash(__name__)

# Estilos CSS personalizados
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Sistema de Gestión Hídrica</title>
        {%favicon%}
        {%css%}
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #87CEEB 0%, #4682B4 50%, #1E90FF 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .main-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .controls-section {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                position: relative;
                z-index: 1000;
            }
            
            .graph-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 25px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .graph-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            }
            
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 25px;
            }
            
            .stat-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: transform 0.3s ease;
            }
            
            .stat-card:hover {
                transform: translateY(-3px);
            }
            
            .control-group {
                margin-bottom: 20px;
            }
            
            .control-label {
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 8px;
                display: block;
                font-size: 14px;
            }
            
            .Select-control {
                border-radius: 10px !important;
                border: 2px solid #e9ecef !important;
                transition: all 0.3s ease !important;
                position: relative !important;
                z-index: 1001 !important;
            }
            
            .Select-menu-outer {
                z-index: 1002 !important;
            }
            
            .VirtualizedSelectFocusedOption {
                z-index: 1003 !important;
            }
            
            .DateInput {
                border-radius: 10px !important;
                position: relative !important;
                z-index: 1001 !important;
            }
            
            .DateRangePickerInput {
                position: relative !important;
                z-index: 1001 !important;
            }
            
            .DateRangePicker {
                z-index: 1004 !important;
            }
            
            .DateRangePicker_picker {
                z-index: 1005 !important;
            }
            
            .Select-control:hover {
                border-color: #0077be !important;
            }
            
            .graph-title {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .icon {
                color: #0077be;
                font-size: 20px;
            }
            
            @media (max-width: 768px) {
                .main-container {
                    padding: 10px;
                }
                
                .header, .controls-section, .graph-container {
                    padding: 15px;
                }
                
                .stats-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1([
                html.I(className="fas fa-tint icon"),
                "Sistema de Gestión Hídrica"
            ], style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'fontSize': '32px',
                'fontWeight': '700',
                'marginBottom': '10px'
            }),
            html.P([
                "Análisis interactivo de estaciones hidrométricas y monitoreo de recursos hídricos"
            ], style={
                'textAlign': 'center',
                'color': '#6c757d',
                'fontSize': '16px',
                'fontWeight': '400'
            })
        ], className="header"),
        
        # Controles
        html.Div([
            html.Div([
                html.Label("Seleccionar Estación", className="control-label"),
                dcc.Dropdown(
                    id='estacion-dropdown',
                    options=[{'label': i, 'value': i} for i in sorted(df['pivot_columns'].dropna().unique())],
                    value=sorted(df['pivot_columns'].dropna().unique())[0],
                    clearable=False,
                    style={
                        'borderRadius': '10px',
                        'border': '2px solid #e9ecef',
                        'fontSize': '14px'
                    }
                ),
            ], className="control-group", style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label("Rango de Fechas", className="control-label"),
                dcc.DatePickerRange(
                    id='fecha-range',
                    min_date_allowed=df['Fecha'].min(),
                    max_date_allowed=df['Fecha'].max(),
                    start_date=df['Fecha'].min(),
                    end_date=df['Fecha'].max(),
                    style={
                        'borderRadius': '10px',
                        'fontSize': '14px'
                    }
                ),
            ], className="control-group", style={'width': '48%', 'float': 'right'}),
        ], className="controls-section"),
        
        # Estadísticas rápidas
        html.Div(id='stats-cards', className="stats-grid"),
        
        # Gráficos
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line icon"),
                "Serie Temporal"
            ], className="graph-title"),
            dcc.Graph(id='serie-temporal')
        ], className="graph-container"),
        
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-box icon"),
                        "Distribución Mensual"
                    ], className="graph-title"),
                    dcc.Graph(id='boxplot-mensual')
                ], style={'width': '50%', 'display': 'inline-block'}),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-bar icon"),
                        "Histograma de Valores"
                    ], className="graph-title"),
                    dcc.Graph(id='histograma')
                ], style={'width': '50%', 'display': 'inline-block'})
            ])
        ], className="graph-container"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-calendar-alt icon"),
                "Evolución Mensual por Año"
            ], className="graph-title"),
            dcc.Graph(id='linea-mensual')
        ], className="graph-container"),
        
        html.Div([
            html.Div([
                html.I(className="fas fa-table icon"),
                "Tabla de Datos"
            ], className="graph-title"),
            html.Div(id='data-table')
        ], className="graph-container")
        
    ], className="main-container")
])

@app.callback(
    [
        Output('serie-temporal', 'figure'),
        Output('boxplot-mensual', 'figure'),
        Output('histograma', 'figure'),
        Output('linea-mensual', 'figure'),
        Output('stats-cards', 'children'),
        Output('data-table', 'children')
    ],
    [
        Input('estacion-dropdown', 'value'),
        Input('fecha-range', 'start_date'),
        Input('fecha-range', 'end_date')
    ]
)
def update_graphs(estacion, start_date, end_date):
    dff = df[(df['pivot_columns'] == estacion) &
             (df['Fecha'] >= pd.to_datetime(start_date)) &
             (df['Fecha'] <= pd.to_datetime(end_date))].copy()
    
    dff['Año'] = dff['Fecha'].dt.year
    dff['Mes'] = dff['Fecha'].dt.month
    dff['Año_Mes'] = dff['Fecha'].dt.to_period('M').astype(str)
    
    # Configuración de tema para gráficos
    template = {
        'layout': {
            'colorway': [COLORS['water'], COLORS['water_light'], COLORS['accent'], COLORS['success']],
            'font': {'family': 'Inter', 'size': 12},
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'xaxis': {'gridcolor': 'rgba(0,0,0,0.1)'},
            'yaxis': {'gridcolor': 'rgba(0,0,0,0.1)'}
        }
    }
    
    # Serie Temporal
    dff_mensual = dff.set_index('Fecha').resample('MS')['valor'].mean()
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=dff['Fecha'], 
        y=dff['valor'], 
        name='Valores Diarios',
        line=dict(color=COLORS['water'], width=1),
        opacity=0.7,
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Valor:</b> %{y:.2f}<extra></extra>'
    ))
    fig1.add_trace(go.Scatter(
        x=dff_mensual.index, 
        y=dff_mensual, 
        name='Promedio Mensual',
        mode='lines+markers',
        line=dict(color=COLORS['accent'], width=3, dash='dash'),
        marker=dict(size=8),
        hovertemplate='<b>Mes:</b> %{x}<br><b>Promedio:</b> %{y:.2f}<extra></extra>'
    ))
    fig1.update_layout(
        height=450,
        margin=dict(l=0, r=0, t=0, b=0),
        template=template,
        hovermode='x unified'
    )
    
    # Boxplot mensual
    fig2 = px.box(
        dff, 
        x='Año_Mes', 
        y='valor',
        color_discrete_sequence=[COLORS['water']]
    )
    fig2.update_traces(
        marker=dict(opacity=0.7),
        boxpoints='outliers'
    )
    fig2.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        template=template,
        xaxis_title="Período",
        yaxis_title="Valor"
    )
    
    # Histograma
    fig3 = px.histogram(
        dff, 
        x='valor', 
        nbins=25,
        color_discrete_sequence=[COLORS['water']]
    )
    fig3.update_traces(opacity=0.7)
    fig3.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        template=template,
        xaxis_title="Valor",
        yaxis_title="Frecuencia"
    )
    
    # Línea mensual por año
    mensual = dff.groupby(['Año', 'Mes'])['valor'].mean().reset_index()
    fig4 = px.line(
        mensual, 
        x='Mes', 
        y='valor', 
        color='Año', 
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        template=template,
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        ),
        xaxis_title="Mes",
        yaxis_title="Valor Promedio"
    )
    
    # Estadísticas como tarjetas
    stats = dff['valor'].describe()
    stats_cards = [
        html.Div([
            html.H3(f"{stats['count']:.0f}", style={'color': COLORS['water'], 'fontSize': '28px', 'fontWeight': '700'}),
            html.P("Total Registros", style={'color': '#6c757d', 'fontSize': '14px'})
        ], className="stat-card"),
        html.Div([
            html.H3(f"{stats['mean']:.2f}", style={'color': COLORS['success'], 'fontSize': '28px', 'fontWeight': '700'}),
            html.P("Promedio", style={'color': '#6c757d', 'fontSize': '14px'})
        ], className="stat-card"),
        html.Div([
            html.H3(f"{stats['max']:.2f}", style={'color': COLORS['danger'], 'fontSize': '28px', 'fontWeight': '700'}),
            html.P("Máximo", style={'color': '#6c757d', 'fontSize': '14px'})
        ], className="stat-card"),
        html.Div([
            html.H3(f"{stats['min']:.2f}", style={'color': COLORS['info'], 'fontSize': '28px', 'fontWeight': '700'}),
            html.P("Mínimo", style={'color': '#6c757d', 'fontSize': '14px'})
        ], className="stat-card")
    ]
    
    # Tabla de datos
    data_table = dash_table.DataTable(
        data=dff.tail(10).to_dict('records'),
        columns=[
            {'name': 'Fecha', 'id': 'Fecha', 'type': 'datetime'},
            {'name': 'Valor', 'id': 'valor', 'type': 'numeric', 'format': {'specifier': '.2f'}},
            {'name': 'Estación', 'id': 'pivot_columns'}
        ],
        style_cell={
            'textAlign': 'center',
            'fontFamily': 'Inter',
            'fontSize': '12px',
            'padding': '12px'
        },
        style_header={
            'backgroundColor': COLORS['water'],
            'color': 'white',
            'fontWeight': '600'
        },
        style_data={
            'backgroundColor': 'rgba(255, 255, 255, 0.8)',
            'color': '#333'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgba(247, 249, 250, 0.8)'
            }
        ]
    )
    
    return fig1, fig2, fig3, fig4, stats_cards, data_table

if __name__ == '__main__':
    print("🌊 Sistema de Gestión Hídrica iniciado")
    print("📊 Dashboard disponible en: http://127.0.0.1:8050")
    app.run(debug=True)