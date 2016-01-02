package graph;

import list.*;

public class Vertex extends Object {
	  protected Object item;
	  protected DList pairs;

		/**
		 * item() return's the Vertex's item.
		 */
	public Object item() {
		return item;
	}
	
	public Vertex (Object o) {
		item = o;
		pairs = new DList();
	}
	
	/**
	 * getAdjList() returns the the DList of pairs.
	 */
	public DList getAdjList() {
		return pairs;
	}
	
	/**
	 * addEdgeToList() add's an object in O(1) time.
	 */
	public void addEdgeToList(Object o) {
		pairs.insertBack(o);
	}
}