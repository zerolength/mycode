from flask import Flask, render_template
import graphviz

from flask import Flask, render_template
import graphviz

app = Flask(__name__)

def create_network_topology():
    # Create a Graphviz object for drawing the topology
    dot = graphviz.Digraph(comment='Network Topology')

    # Add nodes (hosts and routers) to the graph
    dot.node('ohost', 'ohost')
    dot.node('orouter', 'orouter')

    dot.node('phost', 'phost')
    dot.node('prouter', 'prouter')

    dot.node('whost', 'whost')
    dot.node('wrouter', 'wrouter')

    dot.node('yhost', 'yhost')
    dot.node('yrouter', 'yrouter')

    dot.node('core', 'core')  # The core router

    # Add edges (connections) between nodes
    dot.edge('ohost', 'orouter')
    dot.edge('phost', 'prouter')
    dot.edge('whost', 'wrouter')
    dot.edge('yhost', 'yrouter')

    # Connect routers to the core router
    dot.edge('core', 'orouter', label='to-orange-core')
    dot.edge('core', 'prouter', label='to-purple-core')
    dot.edge('core', 'wrouter', label='to-white-core')
    dot.edge('core', 'yrouter', label='to-yellow-core')

    return dot.pipe(format='svg').decode('utf-8')

@app.route('/')
def network_topology():
    graph = create_network_topology()
    return render_template('network_topology.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template
import graphviz

app = Flask(__name__)

def create_network_topology():
    # Create a Graphviz object for drawing the topology
    dot = graphviz.Digraph(comment='Network Topology')

    # Add nodes (hosts and routers) to the graph
    dot.node('ohost', 'ohost')
    dot.node('orouter', 'orouter')

    dot.node('phost', 'phost')
    dot.node('prouter', 'prouter')

    dot.node('whost', 'whost')
    dot.node('wrouter', 'wrouter')

    dot.node('yhost', 'yhost')
    dot.node('yrouter', 'yrouter')

    dot.node('core', 'core')  # The core router

    # Add edges (connections) between nodes
    dot.edge('ohost', 'orouter')
    dot.edge('phost', 'prouter')
    dot.edge('whost', 'wrouter')
    dot.edge('yhost', 'yrouter')

    # Connect routers to the core router
    dot.edge('core', 'orouter', label='to-orange-core')
    dot.edge('core', 'prouter', label='to-purple-core')
    dot.edge('core', 'wrouter', label='to-white-core')
    dot.edge('core', 'yrouter', label='to-yellow-core')

    return dot.pipe(format='svg').decode('utf-8')

@app.route('/')
def network_topology():
    graph = create_network_topology()
    return render_template('network_topology.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
