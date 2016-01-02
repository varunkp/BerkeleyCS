/* HashTable.java */

package graph;

import list.DList;
import list.DListNode;
import list.InvalidNodeException;

/**
 *  HashTable is a hash table with chaining.
 *  All objects used as keys must have a valid hashCode() method, which is
 *  used to determine which bucket of the hash table an entry is stored in.
 *  Each object's hashCode() is presumed to return an int between
 *  Integer.MIN_VALUE and Integer.MAX_VALUE.  The HashTable class
 *  implements only the compression function, which maps the hash code to
 *  a bucket in the table's range.
 *
 *  DO NOT CHANGE ANY PROTOTYPES IN THIS FILE.
 **/

public class HashTable {

  /**
   *  Place any data fields here.
   **/

	protected DList[] table;
	protected int tableSize;
	protected int buckNum;

  /** 
   *  Construct a new empty hash table intended to hold roughly sizeEstimate
   *  entries.  (The precise number of buckets is up to you, but we recommend
   *  you use a prime number, and shoot for a load factor between 0.5 and 1.)
   **/

  public HashTable(int sizeEstimate) {
	  buckNum = (int) Math.round(sizeEstimate) / 3;
	  while (!isPrime (buckNum)) {
		  buckNum++;
	  }
	  table = new DList[buckNum];
          
    // Your solution here.
  }

  /** 
   *  Construct a new empty hash table with a default size.  Say, a prime in
   *  the neighborhood of 100.
   **/

  public HashTable() {
	  table = new DList[101];
  }

  /**
   *  Converts a hash code in the range Integer.MIN_VALUE...Integer.MAX_VALUE
   *  to a value in the range 0...(size of hash table) - 1.
   *
   *  This function should have package protection (so we can test it), and
   *  should be used by insert, find, and remove.
   **/

  int compFunction(int code) {
    // Replace the following line with your solution.
      int convert = Math.abs(((3 * code + 17) % 1234577) % table.length); //randomly chosen prime above 1234567
	  return convert;
  }

  /**
   * Checks if a number is prime. 
   **/

private static boolean isPrime(long n) {
    long x = 2;
    long y = (long) Math.ceil (Math.sqrt(n));    
    if ((n % 2) == 0)
        return false; 
    for (long i = x; i < y; i++) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}
 
  /** 
   *  Returns the number of entries stored in the dictionary.  Entries with
   *  the same key (or even the same key and value) each still count as
   *  a separate entry.
   *  @return number of entries in the dictionary.
   **/

  public int size() {
    // Replace the following line with your solution.
    return tableSize;
  }
  /** 
   *  Tests if the dictionary is empty.
   *
   *  @return true if the dictionary has no entries; false otherwise.
   **/

  public boolean isEmpty() {
    // Replace the following line with your solution.
    return tableSize == 0;
  }

  /**
   *  Create a new Entry object referencing the input key and associated value,
   *  and insert the entry into the dictionary.  Return a reference to the new
   *  entry.  Multiple entries with the same key (or even the same key and
   *  value) can coexist in the dictionary.
   *
   *  This method should run in O(1) time if the number of collisions is small.
   *
   *  @param key the key by which the entry can be retrieved.
   *  @param value an arbitrary object.
   *  @return an entry containing the key and value.
   **/

  public Entry insert(Object key, Object value) {
	  resize();
	  Entry entry = new Entry();
	  entry.key = key;
	  entry.value = value;
	  int buck = compFunction(key.hashCode());
	  if (table[buck] == null) {
              DList newD = new DList();
              newD.insertFront(entry);
          }
          else {
              table[buck].insertFront(entry);
          }

    // Replace the following line with your solution.
          tableSize++;
          return entry;
  }

  /** 
   *  Search for an entry with the specified key.  If such an entry is found,
   *  return it; otherwise return null.  If several entries have the specified
   *  key, choose one arbitrarily and return it.
   *
   *  This method should run in O(1) time if the number of collisions is small.
   *
   *  @param key the search key.
   *  @return an entry containing the key and an associated value, or null if
   *          no entry contains the specified key.
   **/

  public Entry find(Object key) {
	  int buck = compFunction(key.hashCode());
	  DListNode curr = table[buck].front();
	  if (table[buck] != null) {
		  try {
              Entry entry = (Entry) curr.item();
			  while (!key.equals(entry.key())) {
				  curr = curr.next();
			  }
			  entry = (Entry) curr.item();
			  return entry;
		  }
		  catch (InvalidNodeException e1) {
			  return null;
		  }
	  }
	  else {
		  return null;
	  }
    // Replace the following line with your solution.
  }

  /** 
   *  Remove an entry with the specified key.  If such an entry is found,
   *  remove it from the table and return it; otherwise return null.
   *  If several entries have the specified key, choose one arbitrarily, then
   *  remove and return it.
   *
   *  This method should run in O(1) time if the number of collisions is small.
   *
   *  @param key the search key.
   *  @return an entry containing the key and an associated value, or null if
   *          no entry contains the specified key.
   */

  public Entry remove(Object key) {
	  resize();
	  int buck = compFunction(key.hashCode());
	  DListNode curr = table[buck].front();
	  if (table[buck]  != null) {
		  try {
              Entry entry = (Entry) curr.item();
			  while (!key.equals(entry.key())) {
				  curr = curr.next();
			  }
			  entry = (Entry) curr.item();
			  tableSize--;
			  return entry;
		  }
		  catch (InvalidNodeException e1) {
			  return null;
		  }
	  }
	  else {
		  return null;
	  }
    // Replace the following line with your solution.
  }
  
  public void resize() {
	  if ((1.0*tableSize)/buckNum >= 0.75) {
		  buckNum = 2 * buckNum;
	  }
	  else if ((1.0*tableSize)/buckNum <= 0.25) {
		  buckNum = buckNum / 2;
	  }
	  else {
		  return;
	  }
	  while (!isPrime (buckNum)) {
		  buckNum++;
	  }
	  DList[] oldTable = table;
	  table = new DList[buckNum];
	  for (int i = 0; i < oldTable.length; i++) {
		  DList curr = oldTable[i];
		  if (curr != null) {
			  try {
				  DListNode currNode = curr.front();
				  while (currNode.isValidNode()) {
					  Entry entry = (Entry) currNode.item();
					  insert(entry.key(), entry.value());
					  currNode = currNode.next();
				  }
			  }
			  catch (InvalidNodeException e1){
				  System.out.println("Invalid node.");
			  }
		  }
		  else {
			  continue;
		  }
	  }
  }

  /**
   *  Remove all entries from the hash table.
   */
  public void makeEmpty() {
	  table = new DList[table.length - 1];
	  tableSize = 0;
    // Your solution here.
  }
    public void histogram() {
        String hist = "";
        int coll = 0;
        for (int i = 0; i < table.length; i++) {
            if (table[i] == null) {
                hist = hist + "  0";
            }
            else {
                hist = hist + "  " + table[i].length();
                coll = coll +  table[i].length() - 1;
            }
        }
        System.out.println(hist);
        System.out.println("Table size " + table.length);
        System.out.println("Collisions " + coll);
    } 

}
