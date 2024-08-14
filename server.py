import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np

# Sample data

df = pd.read_csv("datasets/financial_data.csv")
df_2=pd.read_csv('datasets/final_demographics_data.csv')
df_2['country'][24]="Occupied Palestine"

gdp=pd.read_csv('datasets/gdp.csv').dropna()
gdp['Country Name'][95]="occupied palestine"
df_2['Arms imports (SIPRI trend indicator values)'].fillna(0,inplace=True)
df_2['Arms exports (SIPRI trend indicator values)'].fillna(0,inplace=True)

df_2_filtred=df_2
df_2_filtred["reserve"]=df_2['Total reserves (includes gold, current US$)']/10e9
df_2_filtred.dropna(subset=['reserve'],inplace=True)

fig=px.bar(df_2_filtred.sort_values('reserve',ascending=False).head(10),x='country',y='reserve',title='top 10 countries Total reserves (includes gold, current US$)')

 




# Initialize the Dash app
font_awesome = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
meta_tags = [{"name": "viewport", "content": "width=device-width"}]
external_stylesheets = [meta_tags, font_awesome]

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
# Define the layout of the dashboard
app.layout = html.Div(children=[
            html.Div([
            html.Img(src = app.get_asset_url('statistics.png'),
                     style = {'height': '50px','padding':'10px'},
                     className = 'title_image'
                     ),
            html.H4('Financial Dashboard',
                    style = {'color': '#D35940'},
                    className = 'title'
                    ),
        ], className = 'logo_title' ,style={'display':'flex','flex-direction':'row','align-items':'center','justify-content':'center'}),
               html.Div([

            dcc.Dropdown(id = 'select_month',
                         multi = False,
                         clearable = True,
                         disabled = True,
                         style = {'display': 'none'},
                         value = 'Mar',
                         placeholder = 'Select Month',
                         options = [{'label': c, 'value': c}
                                    for c in df['months'].unique()],
                         className = 'drop_down_list'),
            
        ], className = 'title_drop_down_list'),

        html.Div([
            dcc.Graph(id='top-richest'),
                        dcc.Dropdown(id = 'select_country',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Algeria',
                         placeholder = 'Select country',
                         options = [{'label': c, 'value': c}
                                    for c in df_2['country'].unique()],
                         className = 'drop_down_list'),
            html.Div([
            dcc.Graph(id='male-female-distribution',style={'width':'30vw'}),
            dcc.Graph(id='urban-distribution',style={'width':'30vw'}),
            dcc.Graph(id='arms-imports',style={'width':'30vw'})],style={'display': 'flex', 'flexDirection': 'row','width':'100vw'}),
            
            html.Div([
            html.Div([
            html.Div([
            html.H2(children='select country'),
            dcc.Dropdown(id = 'select_country2',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True,'width':'20vw'},
                         value = 'Algeria',
                         placeholder = 'Select country',
                         options = [{'label': c, 'value': c}
                                    for c in gdp['Country Name'].unique()],
                         className = 'drop_down_list')
            ],style={"display":"flex","flex-direction":'column','justify-content':'center','align-items':'center'}),
            dcc.Graph(id='gdp-evolution'),
            ],style={'width':'48vw'}),
            html.Div([
                html.Div([
                    html.H2(children='select year'),
                        dcc.Dropdown(id = 'select_year',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True,'width':'20vw'},
                         value = '2022 [YR2022]',
                         placeholder = 'Select year',
                         options = [{'label': c, 'value': c}
                                    for c in gdp.columns[4:]],
                         className = 'drop_down_list'),
                         dcc.Graph(id='gdp-per-year'),],style={"display":"flex","flex-direction":'column','justify-content':'center','align-items':'center'})
                

            ],style={'width':'52vw'})
            ],style={"display":"flex","width":"100vw"})
        ])
      
],)


#define Callbacks

@app.callback(Output('gdp-per-year','figure'),
              [Input('select_year','value')])
def retrieve_revenue(year):
    print(year)
    gdp1 =gdp[gdp[year] != ".."]
    gdp1[year]=gdp1[year].astype(float)/10e8

    
    fig = px.choropleth(
            gdp1.head(190),
            locations='Country Name',
            locationmode='country names',
            color=year,
            title=f'gdp worldwide Heatmap (Billion$)',
            color_continuous_scale='viridis',
             
        )

    return fig

@app.callback(Output('top-richest','figure'),
              [Input('select_month','value')])

def top_richest(val):

    df_2_filtred=df_2
    df_2_filtred["reserve"]=df_2['Total reserves (includes gold, current US$)']/10e9
    df_2_filtred.dropna(subset=['reserve'],inplace=True)

    
    fig=px.bar(
               df_2_filtred.sort_values('reserve',ascending=False).head(10),
               x='country',
               y='reserve',
               title='top 10 countries Total reserves (includes gold, current US$)'
               )


    return fig

@app.callback(Output('male-female-distribution','figure'),
              [Input('select_country','value')])

def sexe_distribution(val):

    labels=['male','female']

    male=df_2[df_2['country']==val]['Population, male'].values[0]

    female=df_2[df_2['country']==val]['Population, female'].values[0]

    fig = fig = go.Figure(data=[go.Pie(labels=labels, values=[male,female], hole=.6,title='male-female distribution')],)

    return fig

@app.callback(Output('urban-distribution','figure'),
              [Input('select_country','value')])

def sexe_distribution(val):
    labels=['urban','non urban ']

    urban=df_2[df_2['country']==val]['Urban population'].values[0]

    non_urban=df_2[df_2['country']==val]['Population, total'].values[0]-df_2[df_2['country']==val]['Urban population'].values[0]

    fig = fig = go.Figure(data=[go.Pie(labels=labels, values=[urban,non_urban], hole=.6,title='population distribution city/countryside  ')])

    return fig

@app.callback(Output('arms-imports','figure'),
              [Input('select_country','value')])

def arms_imports(val):

    labels=['arms exports ','arms imports']

    imports=df_2[df_2['country']==val]['Arms imports (SIPRI trend indicator values)'].values[0]

    exports=df_2[df_2['country']==val]['Arms exports (SIPRI trend indicator values)'].values[0]

    fig = fig = go.Figure(data=[go.Pie(labels=labels, values=[exports,imports], hole=.6,title='weapon imports and exports')])

    return fig


@app.callback(Output('gdp-evolution','figure'),
              [Input('select_country2','value')])

def sexe_distribution(country):

    data=gdp[gdp['Country Name']==country].iloc[:,4:].values[0].astype(float)
    print(data)
    years=np.array([1990,2000,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022])
    df=pd.DataFrame({'data':data,
                     'year':years})
    



    fig = px.line(df,x='year',y='data')

    return fig
 


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
