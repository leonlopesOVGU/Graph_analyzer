import streamlit as st
import json
import graphviz
import uuid
from model import metamodel_dict
from streamlit_agraph import agraph, Node, Edge, Config
import networkx as nx
from graph_function import output_nodes_and_edges, count_nodes, shortest_paths

def upload_graph():
    uploaded_graph = st.file_uploader('upload an existing graph', type='json')
    if uploaded_graph is not None:
        uploaded_graph_dict = json.load(uploaded_graph)
        uploaded_nodes = uploaded_graph_dict['nodes']
        uploaded_edges = uploaded_graph_dict['edges']
        st.json(uploaded_graph_dict, expanded=False)
    else:
        st.info('please upload a graph if available')

    update_graph_button = st.button(
        'update graph via the upload',
        use_container_width=True,
        type='primary'
    )
    if update_graph_button and uploaded_graph is not None:
        st.session_state['node_list'] = uploaded_nodes
        st.session_state['edge_list'] = uploaded_edges
        graph_dict = {
            'nodes': st.session_state['node_list'],
            'edges': st.session_state['edge_list'],
        }
        st.session_state['graph_dict'] = graph_dict

def create_relation():
    def save_edge(node1, relation, node2):
        edge_dict = {
            'source': node1,
            'target': node2,
            'type': relation,
            'id': str(uuid.uuid4()),
        }
        st.session_state['edge_list'].append(edge_dict)
    node1_col, relation_col, node2_col = st.columns(3)
    node_list = st.session_state['node_list']
    node_name_list = []
    for node in node_list:
        node_name_list.append(node['name'])
    with node1_col:
        node1_select = st.selectbox('Select the first node',
                                      options=node_name_list,
                                      key='node1_select'
                                      )
    with relation_col:
        # logic
        relation_list = metamodel_dict['edges'],
        # ui rendering
        relation_name = st.selectbox(
            'specify the relation',
            options=['friends with', 'parent of', 'child of', 'sibling of', 'colleague of']
        )
    with node2_col:
        node2_select = st.selectbox('Select the second node',
                                      options=node_name_list,
                                      key='node2_select'
                                      )
    store_edge_button = st.button('store relation',
                                  use_container_width=True,
                                  type='primary'
                                  )
    if store_edge_button:
        save_edge(node1_select, relation_name, node2_select)

        st.write(f'{node1_select} is {relation_name} {node2_select}')
        st.write(st.session_state['edge_list'])
def create_node():
    def save_node(name, age, type_n):
        node_dict = {
            'name': name,
            'age': age,
            'id':str(uuid.uuid4()),
            'type':type_n
        }
        st.session_state['node_list'].append(node_dict)


    def print_hi(name, age):
        # Use a breakpoint in the code line below to debug your script.
        st.info(f'hi, my name is  {name} and i am {age} years old')  # Press Ctrl+F8 to toggle the breakpoint.

    name_node = st.text_input('type in name of node')
    type_node = st.selectbox(['specify the type of the node','node','person'])
    age_node = int(st.number_input('type in age of the node'))
    print_hi(name_node, age_node)
    save_node_button = st.button('store node', use_container_width=True, type='primary')
    if save_node_button:
        save_node(name_node, age_node)

def store_graph():
    with st.expander('show individual list'):
        st.json(st.session_state['node_list'], expanded=False)
        st.json(st.session_state['edge_list'], expanded=False)

    graph_dict = {
        'nodes': st.session_state['node_list'],
        'edges': st.session_state['edge_list'],
    }
    st.session_state['graph_dict'] = graph_dict

    with st.expander('show graph json', expanded=False):
        st.json(st.session_state['graph_dict'])

def visualize_graph():
    # Create a graphlib graph object
    def set_color(node_type):
        color = 'grey'
        if node_type == ('person'):
            color='blue'
        elif node_type=='node':
            color='green'
        elif node_type=='resource':
            color='violet'
        elif node_type=='sensor':
            color = 'red'
        return color

    with st.expander('graphviz visualisation'):
        graph = graphviz.Digraph()
        graph_dict = st.session_state['graph_dict']
        node_list = graph_dict['nodes']
        edge_list = graph_dict['edges']
        for node in node_list:
            node_name = node['name']
            graph.node(node_name, color= set_color(node_type='node'))
        for edge in edge_list:
            source = edge['source']
            target = edge['target']
            label = edge['type']
            graph.edge(source, target, label)

        st.graphviz_chart(graph)

    with st.expander('AGraph visualisation'):
        nodes = []
        edges = []
        node_list = graph_dict['nodes']
        edge_list = graph_dict['edges']
        for node in node_list:
            nodes.append(Node(id=node['name'],
                              label=node['name'],
                              size=25,
                              #shape="circularImage"
                              ))
        for edge in edge_list:
            edges.append(Edge(source=edge['source'], target=edge['target'], label=edge['type']))

        config = Config(width=750,
                        height=950,
                        directed=True,
                        physics=True,
                        hierarchical=False,
                        # **kwargs
                        )

        return_value = agraph(nodes=nodes,
                              edges=edges,
                              config=config
                              )


def analyze_graph():
    G = nx.Graph()

    graph_dict = st.session_state['graph_dict']
    node_list = graph_dict['nodes']
    edge_list = graph_dict['edges']
    node_tuple_list = []
    edge_tuple_list = []

    for node in node_list:
        node_tuple = (node['name'], node)
        node_tuple_list.append(node_tuple)
    for edge in edge_list:
        edge_tuple = (edge['source'], edge['target'], edge)
        edge_tuple_list.append(edge_tuple)

    G.add_nodes_from(node_tuple_list)
    G.add_edges_from(edge_tuple_list)

    select_function = st.selectbox(label='select function', options=['output nodes and edges', 'count nodes', 'shortest path'])
    if select_function == 'output nodes and edges':
        output_nodes_and_edges(graph=G)
    elif select_function == 'count nodes':
            count_nodes(graph=G)
    elif select_function == 'shortest path':
        shortest_paths(graph=G)

def export_graph():
    graph_string = json.dumps(st.session_state['graph_dict'])

    st.download_button(
        'export graph to json',
        file_name='graph.json',
        mime='application/json',
        data=graph_string,
        use_container_width=True,
        type='primary'
    )




