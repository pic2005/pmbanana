import dash
from dash import dcc, html, dash_table
import dash_leaflet as dl
import pandas as pd
import plotly.express as px
from data import load_pm25_data, load_humidity_data, load_temperature_data, pm25_data

# อ่านข้อมูล
pm25_df = load_pm25_data()
humidity_df = load_humidity_data()
temperature_df = load_temperature_data()

# แปลงคอลัมน์ datetime เป็น datetime object
pm25_df['datetime'] = pd.to_datetime(pm25_df['datetime'])
humidity_df['datetime'] = pd.to_datetime(humidity_df['datetime'])
temperature_df['datetime'] = pd.to_datetime(temperature_df['datetime'])

# คำนวณค่าเฉลี่ยรายวันในช่วง 7 วันที่ผ่านมา
pm25_avg = pm25_df['prediction_label'].mean()
humidity_avg = humidity_df['prediction_label'].mean()
temperature_avg = temperature_df['prediction_label'].mean()

# สร้าง Dash Application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# กำหนดสีและธีม
colors = {
    'background': '#1E1E1E',  # สีพื้นหลังดำ
    'text': '#FFFFFF',        # สีข้อความขาว
    'line_pm25': '#FF69B4',   # สีเส้น PM2.5 (ชมพู)
    'line_humidity': '#00BFFF',  # สีเส้นความชื้น (ฟ้า)
    'line_temperature': '#FF4500'  # สีเส้นอุณหภูมิ (ส้ม)
}

# สร้างกราฟ PM2.5
fig_pm25 = px.line(pm25_df, x='datetime', y='prediction_label', title='PM2.5 Prediction')
fig_pm25.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    title_font_color=colors['text'],
    title_x=0.5
)
fig_pm25.update_traces(
    line=dict(color=colors['line_pm25'], width=2),
    fill='tozeroy',
    fillcolor='rgba(138, 43, 226, 0.1)'  # สีอ่อนกว่าขอบเส้น
)
fig_pm25.update_xaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)
fig_pm25.update_yaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)

# สร้างกราฟความชื้น
fig_humidity = px.line(humidity_df, x='datetime', y='prediction_label', title='Humidity Prediction')
fig_humidity.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    title_font_color=colors['text'],
    title_x=0.5
)
fig_humidity.update_traces(
    line=dict(color=colors['line_humidity'], width=2),
    fill='tozeroy',
    fillcolor='rgba(30, 144, 255, 0.1)'  # สีอ่อนกว่าขอบเส้น
)
fig_humidity.update_xaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)
fig_humidity.update_yaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)

# สร้างกราฟอุณหภูมิ
fig_temperature = px.line(temperature_df, x='datetime', y='prediction_label', title='Temperature Prediction')
fig_temperature.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    title_font_color=colors['text'],
    title_x=0.5
)
fig_temperature.update_traces(
    line=dict(color=colors['line_temperature'], width=2),
    fill='tozeroy',
    fillcolor='rgba(255, 69, 0, 0.1)'  # สีอ่อนกว่าขอบเส้น
)
fig_temperature.update_xaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)
fig_temperature.update_yaxes(gridcolor='rgba(200, 200, 200, 0.5)', gridwidth=0.5)

# Layout ของแอปพลิเคชัน
app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'padding': '20px'},
    children=[
        html.H1("PM2.5 Monitoring Dashboard", style={'textAlign': 'center', 'color': colors['text']}),
        
        # แสดงข้อมูล PM2.5
        html.Div([
            html.H3(f"สถานี: {pm25_data['location']}", style={'color': colors['text']}),
        ]),
        
        # แผนที่
        dl.Map(
            center=[pm25_data['latitude'], pm25_data['longitude']],  # ตำแหน่งศูนย์กลางแผนที่
            zoom=15,  # ระดับการซูม
            style={'width': '100%', 'height': '50vh', 'margin': 'auto', 'border': '2px solid black'},
            children=[
                dl.TileLayer(),  # แสดงแผนที่พื้นหลัง
                dl.Marker(  # แสดง Marker บนแผนที่
                    position=[pm25_data['latitude'], pm25_data['longitude']],
                    children=[
                        dl.Tooltip(f"PM2.5: {pm25_data['pm25']} {pm25_data['unit']}"),  # แสดง Tooltip
                        dl.Popup(f"สถานี: {pm25_data['location']}")  # แสดง Popup
                    ]
                )
            ]
        ),

        # แสดงค่าเฉลี่ยรายวันในช่วง 7 วันที่ผ่านมา
        html.Div([
            html.H3("ค่าเฉลี่ยรายวัน", style={'color': colors['text'], 'marginTop': '20px'}),
            html.Div(
                style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '10px'},
                children=[
                    html.Div(
                        className='average-box',
                        style={'borderColor': colors['line_pm25']},
                        children=[
                            html.H4("PM2.5", style={'color': colors['line_pm25']}),
                            html.P(f"{pm25_avg:.1f} µg/m³", style={'color': colors['line_pm25']})
                        ]
                    ),
                    html.Div(
                        className='average-box',
                        style={'borderColor': colors['line_humidity']},
                        children=[
                            html.H4("ความชื้น", style={'color': colors['line_humidity']}),
                            html.P(f"{humidity_avg:.1f}%", style={'color': colors['line_humidity']})
                        ]
                    ),
                    html.Div(
                        className='average-box',
                        style={'borderColor': colors['line_temperature']},
                        children=[
                            html.H4("อุณหภูมิ", style={'color': colors['line_temperature']}),
                            html.P(f"{temperature_avg:.1f}°C", style={'color': colors['line_temperature']})
                        ]
                    )
                ]
            )
        ]),

        # Dropdown สำหรับเลือกวัน (อยู่ด้านบนของข้อมูลทั้งหมด)
        html.Div([
            html.H3("เลือกวันที่", style={'color': colors['text'], 'marginTop': '30px'}),
            dcc.Dropdown(
                id='date-dropdown',
                options=[{'label': date, 'value': date} for date in pm25_df['datetime'].dt.strftime('%Y-%m-%d').unique()],
                value=pm25_df['datetime'].dt.strftime('%Y-%m-%d').unique()[0],  # เลือกวันแรกเป็นค่าเริ่มต้น
                clearable=False,
                style={'backgroundColor': colors['background'], 'color': colors['text']}
            )
        ]),

        # จัดวางกราฟและข้อมูลที่ทำนายทั้งหมดให้อยู่ข้างกัน
        html.Div(
            style={'display': 'flex', 'marginTop': '20px'},
            children=[
                # ส่วนซ้าย: กราฟ
                html.Div(
                    style={'flex': '2', 'marginRight': '20px'},
                    children=[
                        dcc.Graph(id='pm25-graph', figure=fig_pm25, className='dash-graph'),
                        dcc.Graph(id='humidity-graph', figure=fig_humidity, className='dash-graph'),
                        dcc.Graph(id='temperature-graph', figure=fig_temperature, className='dash-graph')
                    ]
                ),
                # ส่วนขวา: ข้อมูลที่ทำนายทั้งหมด
                html.Div(
                    style={'flex': '1'},
                    children=[
                        html.H3("ข้อมูลที่ทำนายทั้งหมด", style={'color': colors['text']}),
                        dash_table.DataTable(
                            id='prediction-table',
                            columns=[
                                {'name': 'วันที่/เวลา', 'id': 'datetime'},
                                {'name': 'PM2.5 (µg/m³)', 'id': 'pm25'},
                                {'name': 'ความชื้น (%)', 'id': 'humidity'},
                                {'name': 'อุณหภูมิ (°C)', 'id': 'temperature'}
                            ],
                            data=pm25_df.to_dict('records'),
                            style_table={
                                'backgroundColor': '#333333',  # สีเทาเข้ม/ดำเทา
                                'border': '1px solid #444',
                                'borderRadius': '10px',
                                'boxShadow': '4px 4px 10px rgba(0, 0, 0, 0.5)',
                                'overflow': 'hidden'
                            },
                            style_header={
                                'backgroundColor': '#444444',  # สีเทาเข้มกว่าสำหรับหัวตาราง
                                'color': colors['text'],  # สีข้อความขาว
                                'fontWeight': 'bold',
                                'textAlign': 'center',
                                'borderBottom': '2px solid #555'
                            },
                            style_cell={
                                'backgroundColor': '#333333',  # สีพื้นหลังเซลล์เทาเข้ม
                                'color': colors['text'],  # สีข้อความขาว
                                'textAlign': 'center',
                                'border': '1px solid #444',
                                'padding': '10px'
                            },
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': 'pm25'},  # คอลัมน์ PM2.5
                                    'color': colors['line_pm25'],  # สีชมพูตามกราฟ PM2.5
                                    'textAlign': 'right',
                                    'fontFamily': 'Courier New, monospace'
                                },
                                {
                                    'if': {'column_id': 'humidity'},  # คอลัมน์ความชื้น
                                    'color': colors['line_humidity'],  # สีฟ้าตามกราฟความชื้น
                                    'textAlign': 'right',
                                    'fontFamily': 'Courier New, monospace'
                                },
                                {
                                    'if': {'column_id': 'temperature'},  # คอลัมน์อุณหภูมิ
                                    'color': colors['line_temperature'],  # สีส้มตามกราฟอุณหภูมิ
                                    'textAlign': 'right',
                                    'fontFamily': 'Courier New, monospace'
                                },
                                {
                                    'if': {'column_id': 'datetime'},  # คอลัมน์วันที่
                                    'color': colors['text'],  # สีขาว
                                    'textAlign': 'left',
                                    'fontFamily': 'Arial, sans-serif'
                                }
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# เพิ่ม CSS
app.css.append_css({
    'external_url': '/assets/styles.css'
})

# Callback สำหรับอัปเดตตารางเมื่อเลือกวัน
@app.callback(
    dash.dependencies.Output('prediction-table', 'data'),
    [dash.dependencies.Input('date-dropdown', 'value')]
)
def update_table(selected_date):
    # กรองข้อมูลตามวันที่ที่เลือก
    filtered_pm25 = pm25_df[pm25_df['datetime'].dt.strftime('%Y-%m-%d') == selected_date]
    filtered_humidity = humidity_df[humidity_df['datetime'].dt.strftime('%Y-%m-%d') == selected_date]
    filtered_temperature = temperature_df[temperature_df['datetime'].dt.strftime('%Y-%m-%d') == selected_date]

    # รวมข้อมูล
    data = []
    for i in range(len(filtered_pm25)):
        data.append({
            'datetime': filtered_pm25.iloc[i]['datetime'].strftime('%Y-%m-%d %H:%M:%S'),
            'pm25': filtered_pm25.iloc[i]['prediction_label'],
            'humidity': filtered_humidity.iloc[i]['prediction_label'],
            'temperature': filtered_temperature.iloc[i]['prediction_label']
        })
    return data

# รันแอปพลิเคชัน
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)