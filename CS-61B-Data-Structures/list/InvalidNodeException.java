package list;

public class InvalidNodeException extends Exception {

	protected InvalidNodeException(String string) {
		System.out.println (string);
	}

	protected InvalidNodeException() {
		System.out.println ("Invalid Node Exception thrown");
	}

}
