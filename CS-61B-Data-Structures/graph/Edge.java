/* Edge.java */

/**
 * The Edge class represents Edges in a graph. Edges are extensions of Objects
 * and carry as well as references to Nodes for O(1) removal.
 * Edges have a first and second item for the objects inside the two vertices
 * that make up the Edge, and a weight.
 */

package graph;
import list.*;

public class Edge extends Object {
	private Object firstItem;
	private Object secondItem;
	DListNode firstNode;
	DListNode secondNode;
	private int weight;

	public Edge (Object a, Object b, int w) {
		setFirstItem(a);
		setSecondItem(b);
		weight = w;
	}
	/**
	 * getWeight() returns the weight of the edge.
	 */
	public int getWeight() {
		return weight;
	}

	/**
	 * removeRefs() removes the references to both vertices in O(1) time.
	 */
	public void removeRefs() {
		try {
			firstNode.remove();
			secondNode.remove();
		}
		catch(InvalidNodeException e) {
			System.out.println("Invalid nodes");
		}
	}

	/**
	 * getFirstItem() returns the firstItem of the edge.
	 */
	public Object getFirstItem() {
		return firstItem;
	}

	/**
	 * setFirstItem() set the firstItem of the edge.
	 */
	public void setFirstItem(Object firstItem) {
		this.firstItem = firstItem;
	}

	/**
	 * getSecondItem() returns the secondItem of the edge.
	 */
	public Object getSecondItem() {
		return secondItem;
	}

	/**
	 * setFirstItem() sets the firstItem of the edge.
	 */
	public void setSecondItem(Object secondItem) {
		this.secondItem = secondItem;
	}
}
