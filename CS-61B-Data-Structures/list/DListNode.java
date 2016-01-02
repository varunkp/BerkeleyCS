/* DListNode.java */

package list;

/**
 *  A DListNode is a mutable node in a DList (doubly-linked list).
 **/

public class DListNode {

    /**
     *  item references the item stored in the current node.
     *  myList references the List that contains this node.
     *  prev references the previous node in the DList.
     *  next references the next node in the DList.
     *
     **/

    protected Object item;
    protected DList myList;
    protected DListNode prev;
    protected DListNode next;

    /**
     *  DListNode() constructor.
     *  @param i the item to store in the node.
     *  @param l the list this node is in.
     *  @param p the node previous to this node.
     *  @param n the node following this node.
     */
    public DListNode(Object i, DList l, DListNode p, DListNode n) {
        item = i;
        myList = l;
        prev = p;
        next = n;
    }

    /**
     *  isValidNode returns true if this node is valid; false otherwise.
     *  An invalid node is represented by a `myList' field with the value null.
     *  Sentinel nodes are invalid, and nodes that don't belong to a list are
     *  also invalid.
     *
     *  @return true if this node is valid; false otherwise.
     *
     *  Performance:  runs in O(1) time.
     */

    public Object item() throws InvalidNodeException {
        if(!isValidNode()) {
            throw new InvalidNodeException();
        }
        return item;
    }

    public boolean isValidNode() {	
        return myList != null;
    }
    /**
     *  setItem is a mutator method that changes the item field of a
     *  DListNode to the item parameter
     *
     *  @exception InvalidNodeException if this node is not valid
     *
     *  Performance: runs in O(1) time.
     */

    public void setItem(Object item) throws InvalidNodeException {
        if(!isValidNode()) {
            throw new InvalidNodeException();
        }
        this.item = item;
    }

    /**
     *  next() returns the node following this node.  If this node is invalid,
     *  throws an exception.
     *
     *  @return the node following this node.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public DListNode next() throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("next() called on invalid node");
        }
        return next;
    }

    /**
     *  prev() returns the node preceding this node.  If this node is invalid,
     *  throws an exception.
     *
     *  @param node the node whose predecessor is sought.
     *  @return the node preceding this node.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public DListNode prev() throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("prev() called on invalid node");
        }
        return prev;
    }

    /**
     *  insertAfter() inserts an item immediately following this node.  If this
     *  node is invalid, throws an exception.
     *
     *  @param item the item to be inserted.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public void insertAfter(Object item) throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("insertAfter() called on invalid node");
        }
        DListNode nextNode = next;
        DListNode theNewNode = myList.newNode(item, myList, this, nextNode);
        nextNode.prev = theNewNode;
        next = nextNode;
    }

    /**
     *  insertBefore() inserts an item immediately preceding this node.  If this
     *  node is invalid, throws an exception.
     *
     *  @param item the item to be inserted.
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */

    public void insertBefore(Object item) throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("insertBefore() called on invalid node");
        }
        DListNode theNewNode = myList.newNode(item, myList, prev, this);
        DListNode prevNode = prev;
        prevNode.next = theNewNode;
        prev = theNewNode;
    }
    
    public boolean hasNext() throws InvalidNodeException {
    	if(!isValidNode()) {
    		throw new InvalidNodeException("hasNext() called an invalid node");
    	}
    	return next != null || next != myList.head;
    }

    /**
     *  remove() removes this node from its DList.  If this node is invalid,
     *  throws an exception.
     *
     *  @exception InvalidNodeException if this node is not valid.
     *
     *  Performance:  runs in O(1) time.
     */
    public void remove() throws InvalidNodeException {
        if (!isValidNode()) {
            throw new InvalidNodeException("remove() called on invalid node");
        }
        DListNode currentNext = next;
        DListNode currentPrev = prev;
        currentPrev.next = currentNext;
        currentNext.prev = currentPrev;
        myList.size--;

        // Make this node an invalid node, so it cannot be used to corrupt myList.
        myList = null;
        // Set other references to null to improve garbage collection.
        next = null;
        prev = null;
    }

}