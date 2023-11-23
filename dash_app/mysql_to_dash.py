import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import dash_table
from config.database_config import MYSQL_CONFIG

# 创建数据库连接
DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:3306/{MYSQL_CONFIG['database']}"
engine = create_engine(DATABASE_URI)
df = pd.read_sql("SELECT * FROM works", engine)

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'name': c, 'id': c} for c in df.columns],
        page_size=50,
        style_table={'height': 'auto', 'overflowY': 'auto'},
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        style_cell={
            'minWidth': '50px', 'width': '50px', 'maxWidth': '300px',
            'height': 'auto',
            # 'whiteSpace': 'normal',
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_data={
            # 'whiteSpace': 'normal',
            'height': '50px'
        },
        
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
