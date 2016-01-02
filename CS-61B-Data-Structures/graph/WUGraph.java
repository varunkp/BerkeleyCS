/* WUGraph.java */

package graph;

//import java.util.Hashtable;
import list.*;

/**
 * The WUGraph class represents a weighted, undirected graph.  Self-edges are
 * permitted.
 */

public class WUGraph {

	HashTable vertexHash;
	HashTable edgeHash;
	DList vertices;
	DList edges;
	protected int vertexCount;
	protected int edgeCount;

	/**
	 * WUGraph() constructs a graph having no vertices or edges.
	 *
	 * Running time:  O(1).
	 */
	public WUGraph() {
		vertices = new DList();
		edges = new DList();
		vertexCount = 0;
		edgeCount = 0;
		vertexHash = new HashTable();
		edgeHash = new HashTable();
	}

	/**
	 * vertexCount() returns the number of vertices in the graph.
	 *
	 * Running time:  O(1).
	 */
	public int vertexCount() {
		return vertexCount;
	}

	/**
	 * edgeCount() returns the number of edges in the graph.
	 *
	 * Running time:  O(1).
	 */
	public int edgeCount() {
		return edgeCount;
	}

	/**
	 * getVertices() returns an array containing all the objects that serve
	 * as vertices of the graph.  The array's length is exactly equal to the
	 * number of vertices.  If the graph has no vertices, the array has length
	 * zero.
	 *
	 * (NOTE:  Do not return any internal data structure you use to represent
	 * vertices!  Return only the same objects that were provided by the
	 * calling application in calls to addVertex().)
	 *
	 * Running time:  O(|V|).
	 */
	public Object[] getVertices() {
		Object[] verts = new Object[vertexCount];
		DListNode curr = (DListNode) vertices.front();
		try {
			if (vertices.length() == 0) {
				return null;
			}
			else {
				int i = 0;
				while (curr.hasNext()) {
					verts[i] = curr.item();
					curr = curr.next();
					i++;
				}
			}
		}
		catch (InvalidNodeException e1) {
			System.out.println ("Invalid Node.");
		}
		return verts;
	}

	/**
	 * addVertex() adds a vertex (with no incident edges) to the graph.  The
	 * vertex's "name" is the object provided as the parameter "vertex".
	 * If this object is already a vertex of the graph, the graph is unchanged.
	 *
	 * Running time:  O(1).
	 */
	public void addVertex(Object vertex) {
		if (!isVertex (vertex)) {
			Vertex v = new Vertex(vertex);
			//vertices.insertFront(v);
			vertices.insertBack(v);
			//DListNode vNode = vertices.front();
			DListNode vNode = vertices.back();
			Entry entry = vertexHash.insert(vertex, vNode); //needs to be returned?
			vertexCount++;
		}
	}

	/**
	 * removeVertex() removes a vertex from the graph.  All edges incident on the
	 * deleted vertex are removed as well.  If the parameter "vertex" does not
	 * represent a vertex of the graph, the graph is unchanged.
	 *
	 * Running time:  O(d), where d is the degree of "vertex".
	 */
	//NEEDS WORK
	//NEEDS WORK

	//NEEDS WORK

	//NEEDS WORK

	//NEEDS WORK

	//NEEDS WORK

	public void removeVertex(Object vertex) {
		//Find the node
		//it walks down the list and removes all the edges.
		//it removes this node.
		Entry entry = vertexHash.remove(vertex);
		try {
			if(vertexHash.find(vertex) != null) {
				DListNode vNode = (DListNode)vertexHash.remove(vertex).value();
				DList pairs = ((Vertex)vNode.item()).getAdjList();
				Vertex v = (Vertex)vNode.item();
				VertexPair temp;
				if(!pairs.isEmpty()) {
					DListNode pointer = pairs.front();
					temp = (VertexPair)pointer.item();
					while(pointer.hasNext()) {
						removeEdge(temp.object1, temp.object2);
						pointer = pointer.next();
						temp = (VertexPair)pointer.item();
					}
					
					removeEdge(temp.object1, temp.object2);
					vertexCount--;
				}
			}
			
		}
		catch (InvalidNodeException e ){
			System.out.println ("Curr has no next.");
		}
		vertexCount--;
	}

	/**
	 * isVertex() returns true if the parameter "vertex" represents a vertex of
	 * the graph.
	 *
	 * Running time:  O(1).
	 */
	public boolean isVertex(Object vertex) {
		return vertexHash.find(vertex) != null;
	}

	/**
	 * degree() returns the degree of a vertex.  Self-edges add only one to the
	 * degree of a vertex.  If the parameter "vertex" doesn't represent a vertex
	 * of the graph, zero is returned.
	 *
	 * Running time:  O(1).
	 */
	public int degree(Object vertex) {
		int d = 0;
		Entry entry = vertexHash.find(vertex);
		if (entry != null) {
			Vertex v = (Vertex) entry.value();
			d = v.pairs.length();
		}
		return d;
	}

	/**
	 * getNeighbors() returns a new Neighbors object referencing two arrays.  The
	 * Neighbors.neighborList array contains each object that is connected to the
	 * input object by an edge.  The Neighbors.weightList array contains the
	 * weights of the corresponding edges.  The length of both arrays is equal to
	 * the number of edges incident on the input vertex.  If the vertex has
	 * degree zero, or if the parameter "vertex" does not represent a vertex of
	 * the graph, null is returned (instead of a Neighbors object).
	 *
	 * The returned Neighbors object, and the two arrays, are both newly created.
	 * No previously existing Neighbors object or array is changed.
	 *
	 * (NOTE:  In the neighborList array, do not return any internal data
	 * structure you use to represent vertices!  Return only the same objects
	 * that were provided by the calling application in calls to addVertex().)
	 *
	 * Running time:  O(d), where d is the degree of "vertex".
	 */
	public Neighbors getNeighbors(Object vertex) {
		DListNode vNode = (DListNode)vertexHash.find(vertex).value();
		try {
			DList pairs = ((Vertex)vNode.item()).getAdjList();
			Object vertexObj = ((Vertex)vNode.item()).item();
			Object[] objs = new Object[pairs.length()];
			int[] weights = new int[pairs.length()];
			DListNode pointer = pairs.front();
			Object pairObj = pointer.item();
			int i = 0;
			Edge e = (Edge)edgeHash.find(new VertexPair(vertex, pairObj)).key();

			while(pointer.hasNext()) {
				objs[i] = pairObj;
				weights[i] = e.getWeight();
				i++;
				pointer = pointer.next();
				pairObj = pointer.item();
				e = (Edge)edgeHash.find(new VertexPair(vertex, pairObj)).key();
			}
			objs[i] = pairObj;
			weights[i] = e.getWeight();
			Neighbors n = new Neighbors();
			n.neighborList = objs;
			n.weightList = weights;

			return n;
		}
		catch(InvalidNodeException e) {
			System.out.println("Invalid node");
		}
		return null;
	}

	/**
	 * addEdge() adds an edge (u, v) to the graph.  If either of the parameters
	 * u and v does not represent a vertex of the graph, the graph is unchanged.
	 * The edge is assigned a weight of "weight".  If the edge is already
	 * contained in the graph, the weight is updated to reflect the new value.
	 * Self-edges (where u == v) are allowed.
	 *
	 * Running time:  O(1).
	 */
	public void addEdge(Object u, Object v, int weight) {
		if (vertexHash.find(u) != null && vertexHash.find(v) != null) {
			VertexPair p = new VertexPair (u,v);
			if(edgeHash.find(p) == null) {
				Edge e = new Edge(u, v, weight);
				edgeHash.insert(p, e);
				edgeCount++;
			}
		}
	}

	/**
	 * removeEdge() removes an edge (u, v) from the graph.  If either of the
	 * parameters u and v does not represent a vertex of the graph, the graph
	 * is unchanged.  If (u, v) is not an edge of the graph, the graph is
	 * unchanged.
	 *
	 * Running time:  O(1).
	 */
	public void removeEdge(Object u, Object v) {
		if (isEdge(u,v)) {
			VertexPair p = new VertexPair (u,v);
			Edge e = (Edge)edgeHash.remove(p).value();
			if (e != null) {
				e.removeRefs();
				edgeCount--;
			}
		}
	}

	/**
	 * isEdge() returns true if (u, v) is an edge of the graph.  Returns false
	 * if (u, v) is not an edge (including the case where either of the
	 * parameters u and v does not represent a vertex of the graph).
	 *
	 * Running time:  O(1).
	 */
	public boolean isEdge(Object u, Object v) {
		VertexPair p = new VertexPair (u,v);
		return edgeHash.find(p) != null;
	}

	/**
	 * weight() returns the weight of (u, v).  Returns zero if (u, v) is not
	 * an edge (including the case where either of the parameters u and v does
	 * not represent a vertex of the graph).
	 *
	 * (NOTE:  A well-behaved application should try to avoid calling this
	 * method for an edge that is not in the graph, and should certainly not
	 * treat the result as if it actually represents an edge with weight zero.
	 * However, some sort of default response is necessary for missing edges,
	 * so we return zero.  An exception would be more appropriate, but
	 * also more annoying.)
	 *
	 * Running time:  O(1).
	 */
	public int weight(Object u, Object v) {
		VertexPair p = new VertexPair(u, v);
		Edge e = (Edge)edgeHash.find(p).value();
		if(e == null) {
			return 0;
		}
		
		return e.getWeight();
	}

}
