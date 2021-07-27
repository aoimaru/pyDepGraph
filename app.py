try:
    import pandas as pd
except ImportError as e:
    print(e)

try:
    import dash
    from dash.dependencies import Input, Output
    import dash_core_components as dcc
    import dash_html_components as html

    import dash_cytoscape as cyto
except ImportError as e:
    print(e)

try:
    import json
    import networkx as nx
    import matplotlib.pyplot as plt
except ImportError as e:
    print(e)



Nodes = []

def extract(datas):
    for data in datas:
        if data["dependencies"]:
            for depData in data["dependencies"]:
                Nodes.append([data["package_name"], depData["package_name"]])
            extract(data["dependencies"])



def read_data():
    with open("./pipDep.json", mode="r") as f:
        datas = json.load(f)

    return datas

def prepares(Nodes):
    froms = [Node[0] for Node in Nodes]
    tos = [Node[1] for Node in Nodes]
    items = pd.DataFrame.from_dict({'from':froms, 'to': tos})
    return items



app = dash.Dash(__name__)
server = app.server


datas = read_data()
extract(datas)
for Node in Nodes:
    print(Node)
edges = prepares(Nodes)


nodes = set()

cy_edges = []
cy_nodes = []

for index, row in edges.iterrows():
    source, target = row['from'], row['to']

    if source not in nodes:
        nodes.add(source)
        cy_nodes.append({"data": {"id": source, "label": source}})
    if target not in nodes:
        nodes.add(target)
        cy_nodes.append({"data": {"id": target, "label": target}})

    cy_edges.append({
        'data': {
            'source': source,
            'target': target
        }
    })

# define stylesheet
stylesheet = [
    {
        "selector": 'node', # すべてのnodeに対して
        'style': {
            "opacity": 0.9,
            "label": "data(label)", # 表示させるnodeのラベル
            "background-color": "#07ABA0", # nodeの色
            "color": "#008B80" # nodeのラベルの色
        }
    },
    {
        "selector": 'edge', # すべてのedgeに対して
        "style": {
            "target-arrow-color": "#C5D3E2", # 矢印の色
            "target-arrow-shape": "triangle", # 矢印の形
            "line-color": "#C5D3E2", # edgeのcolor
            'arrow-scale': 1, # 矢印のサイズ
            'curve-style': 'bezier' # デフォルトのcurve-styleだと矢印が表示されないため指定する
    }
}]

# define layout
app.layout = html.Div([
    dcc.Dropdown(
            id='dropdown-layout',
            options=[
                {'label': 'random',
                 'value': 'random'},
                {'label': 'grid',
                 'value': 'grid'},
                {'label': 'circle',
                 'value': 'circle'},
                {'label': 'concentric',
                 'value': 'concentric'},
                {'label': 'breadthfirst',
                 'value': 'breadthfirst'},
                {'label': 'cose',
                 'value': 'cose'}
            ], value='grid'
        ),
    html.Div(children=[
        cyto.Cytoscape(
            id='cytoscape',
            elements=cy_edges + cy_nodes,
            style={
                'height': '95vh',
                'width': '100%'
            },
            stylesheet=stylesheet
        )
    ])
])

@app.callback(Output('cytoscape', 'layout'),
              [Input('dropdown-layout', 'value')])
def update_cytoscape_layout(layout):
    return {'name': layout}

if __name__ == '__main__':
    datas = read_data()
    app.run_server(host='0.0.0.0', port=8050, debug=True)





