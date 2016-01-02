/* Kruskal.java */

import graph.*;
import set.*;

/**
 * The Kruskal class contains the method minSpanTree(), which implements
 * Kruskal's algorithm for computing a minimum spanning tree of a graph.
 */

public class Kruskal {

	private static WUGraph t;
	private static HashTable vertexHash;
	private static Object[] vertices;
	private static KruskalEdge[] edges;
	private static DisjointSets d;

	/**
	 * minSpanTree() returns a WUGraph that represents the minimum spanning tree
	 * of the WUGraph g.  The original WUGraph g is NOT changed.
	 */
	public static WUGraph minSpanTree(WUGraph g) {
		t = new WUGraph();
		vertexHash = new HashTable();
		vertices = g.getVertices();
		for (int i = 0; i < vertices.length; i++) {
			t.addVertex(vertices[i]);
			vertexHash.insert(vertices[i], new Integer(i));
		}
		edges = getEdges(g); //helper method for all edges in WUGraph
		quicksort(edges); //sort edges
		d = new DisjointSets(vertices.length);
		for (int k = 0; k < edges.length; k++) {
			KruskalEdge e = edges[k];
			//			KruskalVertex v1 = (KruskalVertex) e.getFirstItem();
			//			KruskalVertex v2 = (KruskalVertex) e.getSecondItem();
			//			if (d.find(v1.vKey) != d.find(v2.vKey)) { //
			//				t.addEdge(e.firstItem, e.secondItem, e.weight);
			//				d.union(d.find(v1.vKey), d.find(v2.vKey));
			//			}
			//int v1 = (Integer) vertexHash.find(((KruskalEdge) e.getFirstItem()).value()).intValue();
			//int v1 = vertexHash.find(e.firstItem);
			//int v2 = vertexHash.find(e.secondItem);
			int v1 = ((Integer) vertexHash.find(e.firstItem).value()).intValue();
			int v2 = ((Integer) vertexHash.find(e.secondItem).value()).intValue();
			if (d.find(v1) != d.find(v2)) {
				t.addEdge(e.firstItem, e.secondItem, e.weight);
				d.union(d.find(v1), d.find(v2));
			}
		}
		return t;

		//TO-DO
	}

	/**
	 * quicksort() performs the quickSort sorting algorithm on a KruskalEdge array
	 * by using a helper method.
	 */
	public static void quicksort(KruskalEdge[] a) {
		quicksort(a, 0, a.length - 1);
	}

	/**
	 *  Method to swap two ints in an array.
	 *  @param a an array of ints.
	 *  @param index1 the index of the first int to be swapped.
	 *  @param index2 the index of the second int to be swapped.
	 **/
	public static void swapReferences(KruskalEdge[] a, int index1, int index2) {
		int tmp = a[index1].weight;
		a[index1] = a[index2];
		a[index2].weight = tmp;
	}

	/**
	 *  This is a generic version of C.A.R Hoare's Quick Sort algorithm.  This
	 *  will handle arrays that are already sorted, and arrays with duplicate
	 *  keys.
	 *
	 *  If you think of an array as going from the lowest index on the left to
	 *  the highest index on the right then the parameters to this function are
	 *  lowest index or left and highest index or right.  The first time you call
	 *  this function it will be with the parameters 0, a.length - 1.
	 *
	 *  @param a       an integer array
	 *  @param lo0     left boundary of array partition
	 *  @param hi0     right boundary of array partition
	 **/
	private static void quicksort(KruskalEdge a[], int lo0, int hi0) {
		int lo = lo0;
		int hi = hi0;
		int mid;

		if (hi0 > lo0) {

			// Arbitrarily establishing partition element as the midpoint of
			// the array.
			swapReferences(a, lo0, (lo0 + hi0)/2);
			mid = a[(lo0 + hi0) / 2].weight;

			// loop through the array until indices cross.
			while (lo <= hi) {
				// find the first element that is greater than or equal to 
				// the partition element starting from the left Index.
				while((lo < hi0) && (a[lo].weight < mid)) {
					lo++;
				}

				// find an element that is smaller than or equal to 
				// the partition element starting from the right Index.
				while((hi > lo0) && (a[hi].weight > mid)) {
					hi--;
				}
				// if the indices have not crossed, swap them.
				if (lo <= hi) {
					swapReferences(a, lo, hi);
					lo++;
					hi--;
				}
			}

			// If the right index has not reached the left side of array
			// we must now sort the left partition.
			if (lo0 < hi) {
				quicksort(a, lo0, hi);
			}

			// If the left index has not reached the right side of array
			// must now sort the right partition.
			if (lo < hi0) {
				quicksort(a, lo, hi0);
			}
		}
	}

	/**
	 * getEdges() returns an array of all the Edges in a graph
	 * by iterating through all vertices and their neighbors.
	 * Edges are only added if they have not already been placed
	 * in the array.
	 */
	private static KruskalEdge[] getEdges(WUGraph g) {
		KruskalEdge[] edges = new KruskalEdge[g.edgeCount()];
		HashTable kruskalHash = new HashTable();	
		Object[] vertices = g.getVertices();
		int index = 0;
		for (int i = 0; i < vertices.length; i++) {
			Neighbors nList = g.getNeighbors(vertices[i]);
			for (int j = 0; j < nList.neighborList.length; j++) {
				KruskalEdge ke = new KruskalEdge (vertices[i], nList.neighborList[j], nList.weightList[j]);
				if (kruskalHash.find(ke) == null) {
					edges[index] = ke;
					kruskalHash.insert(ke.firstItem, ke.secondItem);
					index++;
				}
			}
		}
		return edges;
	}

}
