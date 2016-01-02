/* KruskalVertex.java */

public class KruskalVertex {
	protected Object item;
	private static int vertexCount = 0;
	protected int vKey;
	
	
	public KruskalVertex (Object o) {
		item = o;
		vKey= vertexCount;
		vertexCount++;
	}
}