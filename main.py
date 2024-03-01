import streamlit as st
from streamlit_option_menu import option_menu
from tabs import upload_graph, create_relation,create_node,store_graph,visualize_graph,analyze_graph,export_graph



st.set_page_config(layout='wide', initial_sidebar_state='expanded')
if __name__ == '__main__':
    if 'node_list' not in st.session_state:
        st.session_state['node_list'] = []
    if 'edge_list' not in st.session_state:
        st.session_state['edge_list'] = []
    if 'graph_dict' not in st.session_state:
        st.session_state['graph_dict'] = []


    st.title('PyInPSE Tutorial 1')
    tab_list = [
                'import graph',
                'create nodes',
                'create relations between nodes',
                'store the Graph',
                'visualize the graph',
                'analyze the graph',
                'export the Graph'
                ]

    with st.sidebar:
        selected_tab = option_menu('Main Menu',
                                tab_list,
                                icons=['house', 'gear'],
                                menu_icon="cast",
                                default_index=0)
        st.write(selected_tab)

    if selected_tab == 'import graph':
        upload_graph()

    if selected_tab == 'create nodes':
         create_node()

    if selected_tab == 'create relations between nodes':
        create_relation()

    if selected_tab == 'store the Graph':
       store_graph()

    if selected_tab == 'visualize the graph':
        visualize_graph()

    if selected_tab == 'analyze the graph':
        analyze_graph()

    if selected_tab == 'export the Graph':
         export_graph()


