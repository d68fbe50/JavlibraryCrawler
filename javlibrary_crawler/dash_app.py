import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
from arguments import db_path

# 连接到 SQLite 数据库并读取 'spider' 表
conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM spider", conn)

# 处理 release_date，提取年份
df['year'] = pd.to_datetime(df['release_date']).dt.year

# 拆分 'cast' 列并展开
df_cast = df['cast'].str.split(',').explode().str.strip()

# 创建 Dash 应用
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("JavCraw Analysis with Dash"),

    # 下拉菜单选择统计维度
    dcc.Dropdown(
        id='dimension-dropdown',
        options=[
            {'label': 'Year', 'value': 'year'},
            {'label': 'Cast', 'value': 'cast'},
            {'label': 'Label', 'value': 'label'}
        ],
        value='year'
    ),

    # 展示统计结果
    dcc.Graph(id='dimension-analysis')
])

@app.callback(
    Output('dimension-analysis', 'figure'),
    [Input('dimension-dropdown', 'value')]
)
def update_analysis(selected_dimension):
    if selected_dimension == 'cast':
        counts = df_cast.value_counts()
    else:
        counts = df[selected_dimension].value_counts()

    return {
        'data': [{
            'x': counts.index,
            'y': counts.values,
            'type': 'bar'
        }],
        'layout': {
            'title': f'Counts by {selected_dimension}'
        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)
