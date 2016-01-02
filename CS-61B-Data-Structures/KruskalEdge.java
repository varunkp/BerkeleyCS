/*KruskalEdge.java */

	/**
	 * The KruskalEdge class is the companion to the Edge class in the graph package.
	 * KruskalEdge is needed to fulfill the rules of encapsulation.
	 * KruskalEdge will be used in Kruskal.
	 */

public class KruskalEdge implements Comparable {
	protected Object firstItem;
	protected Object secondItem;
	protected int weight;
	
	/**
	 * Necessary.
	 */
	public int compareTo(Object o) {
		if (this.weight == ((KruskalEdge) o).weight){
			return 0;
		} else if (this.weight < ((KruskalEdge) o).weight) {
			return -1;
		} else {
			return 1;
		}

	}
	
	public KruskalEdge (Object a, Object b, int w) {
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
	
	/**
	 * equalEdge() checks if the Edge has already been added through it's half-edge pair.
	 */
	public boolean equalEdge (Object o1, Object o2) {
		if ((o1 == this.firstItem && o2 == this.secondItem) || (o2 == this.firstItem && o1 == this.secondItem)){
			return true;
		}
		else {
			return false;
		}
	}
}