/*
 *
 * CS61C Spring 2013 Project 2: Small World
 *
 * Partner 1 Name: Alex Hsu
 * Partner 1 Login: cs61c-hw
 *
 * Partner 2 Name: Varun Pemmaraju
 * Partner 2 Login: cs61c-gw
 *
 * REMINDERS: 
 *
 * 1) YOU MUST COMPLETE THIS PROJECT WITH A PARTNER.
 * 
 * 2) DO NOT SHARE CODE WITH ANYONE EXCEPT YOUR PARTNER.
 * EVEN FOR DEBUGGING. THIS MEANS YOU.
 *
 */

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;
import java.lang.Math;
import java.util.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Writable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;


public class SmallWorld {
    // Maximum depth for any breadth-first search
    public static final int MAX_ITERATIONS = 20;
    public static final long INF = Long.MAX_VALUE;


    // Example writable type
    public static class NodeValue implements Writable {
  
        public LongWritable distance;
	public LongWritable source;
	public boolean visited;
	public ArrayList<LongWritable> neighbors;

	public NodeValue() {
	}
	
	public NodeValue(LongWritable distance, LongWritable source,  boolean visited, ArrayList<LongWritable> neighbors) {
	    this.distance = distance;
	    this.source = source;
	    this.visited = visited;
	    this.neighbors = neighbors;
	}

	public NodeValue(LongWritable distance, LongWritable source) {
	    this.distance = distance;
	    this.source = source;
	    this.visited = false;
	    this.neighbors = new ArrayList<LongWritable>();
	}
	
        public LongWritable getDistance() {
	    return distance;
	}
	
	public LongWritable getSource() {
	    return source;
	}

	public boolean getVisited() {
	    return visited;
	}

	public ArrayList<LongWritable> getNeighbors() {
	    return neighbors;
	}

	public void setDistance(LongWritable d) {
	    distance = d;
	}

	public void setSource(LongWritable s) {
	    source = s;
	}

	public void setVisited(boolean v) {
	    visited = v;
	}
	
	public void setNeighbors(ArrayList<LongWritable> n) {
	    neighbors = n;
	}

	// Serializes object - needed for Writable
        public void write(DataOutput out) throws IOException {

            out.writeLong(distance.get());
	    out.writeLong(source.get());
	    out.writeBoolean(visited);

	    int length = 0;

	    if (neighbors != null) {
		length = neighbors.size();
	    }
	    out.writeInt(length);
	
	    for (int i = 0; i < length; i++) {
		out.writeLong(neighbors.get(i).get());
	    }
        }
	
	// Deserializes object - needed for Writable
        public void readFields(DataInput in) throws IOException {

	    distance = new LongWritable(in.readLong());
	    source = new LongWritable(in.readLong());
	    visited = in.readBoolean();

	    int length = in.readInt();
	    neighbors = new ArrayList<LongWritable>(length);
	    for (int i = 0; i < length; i++) {
		neighbors.add(new LongWritable(in.readLong()));
	    }
        }
	
        public String toString() {
	    // We highly recommend implementing this for easy testing and
	    // debugging. This version just returns an empty string.
	    String str = "(" + distance + ", " + source + ", " + visited + ", [";

	    for (LongWritable neighbor : neighbors) {
		str += neighbor.get();
		str += ", ";
	    }

	    str += "])";
	    return str;
	}
	
    }
    
    
    /* The first mapper. Part of the graph loading process, currently just an 
     * identity function. Modify as you wish. */
    public static class LoaderMap extends Mapper<LongWritable, LongWritable, 
					  LongWritable, LongWritable> {
	
	@Override
	public void map(LongWritable key, LongWritable value, Context context)
	    throws IOException, InterruptedException {
	   
	    // System.out.println(key);
	    // System.out.println(value);
	   
	    context.write(key, value);
	    context.write(value, new LongWritable(-1L));
	    
	    // example of getting value passed from main
	    // int inputValue = Integer.parseInt(context.getConfiguration().get("inputValue"));
	    
        }
    }
	
	
    /* The first reducer. This is also currently an identity function (although it
     * does break the input Iterable back into individual values). Modify it
     * as you wish. In this reducer, you'll also find an example of loading
     * and using the denom field.  
     */
    public static class LoaderReduce extends Reducer<LongWritable, LongWritable, 
					     LongWritable, NodeValue> {
	
        public long denom;
	
	@Override
        public void reduce(LongWritable key, Iterable<LongWritable> values, Context context)
	    throws IOException, InterruptedException {	    
	    
	    // We can grab the denom field from context: 
            denom = Long.parseLong(context.getConfiguration().get("denom"));
	    
	    // You can print it out by uncommenting the following line:
	    // System.out.println(denom);
	    
	    LongWritable distance = new LongWritable(INF);
	    LongWritable source = new LongWritable(INF);
	    boolean visited = false;
	    ArrayList<LongWritable> neighbors = new ArrayList<LongWritable>();

	    for (LongWritable value : values) {
		if (value.get() != -1L) {
		    neighbors.add(new LongWritable(value.get()));
		}
	    }
	    
	    // System.out.println(neighbors);
	    
	    NodeValue nValue = new NodeValue(distance, source, visited, neighbors);
	    
	    // System.out.println(key);
	    // System.out.println(nValue);
	    
	    context.write(key, nValue);

	    if (Math.random() < (1.0 / denom)) {
		nValue.setDistance(new LongWritable(0L));
		nValue.setSource(key);
	
		// System.out.println(key);
		// System.out.println(nValue);
		
		context.write(key, nValue);
	    }
        }
		
    }

	
    /* The second mapper. Calculate distances via BFS. */
    public static class BFSMap extends Mapper<LongWritable, NodeValue, 
				       LongWritable, NodeValue> {
	
	@Override
	public void map(LongWritable key, NodeValue value, Context context)
	    throws IOException, InterruptedException {
	    
	    if ((value.getDistance().get() != INF) && !value.getVisited()) {
		value.setVisited(true);
		// System.out.println(key);
		// System.out.println(value);
		context.write(key, value);
		for (LongWritable neighbor : (ArrayList<LongWritable>) value.getNeighbors()) {
		    NodeValue nValue = new NodeValue(new LongWritable(value.getDistance().get() + 1), value.getSource());
		    // System.out.println(neighbor);
		    // System.out.println(nValue);
		    context.write(neighbor, nValue);
		}
	    }
	    else {
		// System.out.println(key);
		// System.out.println(value);
		context.write(key, value);
	    }
        }

    }

		
    /* The second reducer. */
    public static class BFSReduce extends Reducer<LongWritable, NodeValue, 
					  LongWritable, NodeValue> {
	
        @Override
	public void reduce(LongWritable key, Iterable<NodeValue> values, Context context)
	    throws IOException, InterruptedException {
	    
	    HashMap<LongWritable,LongWritable> minDist = new HashMap<LongWritable,LongWritable>();
	    // System.out.println(minDist);
	    HashMap<LongWritable,Boolean> visited = new HashMap<LongWritable,Boolean>();
	    // System.out.println(visited);
	    ArrayList<LongWritable> neighbors = new ArrayList<LongWritable>();
	 
	    for (NodeValue value : values) {
		if (value.getSource().get() == INF) {
		    neighbors = value.getNeighbors();
		    context.write(key, value);
		} else if ((value.getSource().get() != INF) &&
		    ((minDist.get(value.getSource()) == null) ||
		     (value.getDistance().get() < minDist.get(value.getSource()).get()))) {
		    minDist.put(value.getSource(), value.getDistance());
		    visited.put(value.getSource(), value.getVisited());
		}	
	    }  
	    // System.out.println(minDist);
	    // System.out.println(visited);
	    for (LongWritable source : minDist.keySet()) {
		NodeValue nValue = new NodeValue(minDist.get(source), source, visited.get(source), neighbors);
		// System.out.println(nValue);
		context.write(key, nValue);
	    }
        }
	
    }

	
    /* The third mapper. */
    public static class HistMap extends Mapper<LongWritable, NodeValue, 
					LongWritable, LongWritable> {
	
	public static LongWritable ONE = new LongWritable(1L);
	
	@Override
        public void map(LongWritable key, NodeValue value, Context context)
	    throws IOException, InterruptedException {
	    
	    if (value.getSource().get() != INF) {
   		context.write(value.getDistance(), ONE);
	    }
	}

    }

		
    /* The third reducer. */
    public static class HistReduce extends Reducer<LongWritable, LongWritable, 
					   LongWritable, LongWritable> {
	
	@Override
        public void reduce(LongWritable key, Iterable<LongWritable> values, Context context)
	    throws IOException, InterruptedException {
            
	    long sum = 0L;
	    
            for (LongWritable value : values){            
		sum += value.get();
            }

	    context.write(key, new LongWritable(sum));
        }
	
    }

	
    public static void main(String[] rawArgs) throws Exception {
        GenericOptionsParser parser = new GenericOptionsParser(rawArgs);
        Configuration conf = parser.getConfiguration();
        String[] args = parser.getRemainingArgs();
		
	// Pass in denom command line arg:
        conf.set("denom", args[2]);
	
	// Sample of passing value from main into Mappers/Reducers using
	// conf. You might want to use something like this in the BFS phase:
	// See LoaderMap for an example of how to access this value
        // conf.set("inputValue", (new Integer(5)).toString());
	
	// Setting up mapreduce job to load in graph
        Job job = new Job(conf, "load graph");
	job.setNumReduceTasks(48);
        job.setJarByClass(SmallWorld.class);
		
        job.setMapOutputKeyClass(LongWritable.class);
        job.setMapOutputValueClass(LongWritable.class);
        job.setOutputKeyClass(LongWritable.class);
        job.setOutputValueClass(NodeValue.class);
		
        job.setMapperClass(LoaderMap.class);
        job.setReducerClass(LoaderReduce.class);
		
        job.setInputFormatClass(SequenceFileInputFormat.class);
        job.setOutputFormatClass(SequenceFileOutputFormat.class);
		
	// Input from command-line argument, output to predictable place
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path("bfs-0-out"));
	
	// Actually starts job, and waits for it to finish
        job.waitForCompletion(true);
	
	// Repeats your BFS mapreduce
        int i = 0;
        while (i < MAX_ITERATIONS) {
	    job = new Job(conf, "bfs" + i);
	    job.setNumReduceTasks(48);
            job.setJarByClass(SmallWorld.class);
			
	    // Feel free to modify these four lines as necessary:
            job.setMapOutputKeyClass(LongWritable.class);
            job.setMapOutputValueClass(NodeValue.class);
            job.setOutputKeyClass(LongWritable.class);
            job.setOutputValueClass(NodeValue.class);
	    
	    // You'll want to modify the following based on what you call
	    // your mapper and reducer classes for the BFS phase.
            job.setMapperClass(BFSMap.class); // currently the default Mapper
            job.setReducerClass(BFSReduce.class); // currently the default Reducer
	    
            job.setInputFormatClass(SequenceFileInputFormat.class);
            job.setOutputFormatClass(SequenceFileOutputFormat.class);
	    
	    // Notice how each mapreduce job gets gets its own output dir
            FileInputFormat.addInputPath(job, new Path("bfs-" + i + "-out"));
            FileOutputFormat.setOutputPath(job, new Path("bfs-"+ (i+1) +"-out"));
	    
            job.waitForCompletion(true);
            i++;
        }
	
	// Mapreduce config for histogram computation
        job = new Job(conf, "hist");
	job.setNumReduceTasks(1);
        job.setJarByClass(SmallWorld.class);
	
	// Feel free to modify these two lines as necessary:
        job.setMapOutputKeyClass(LongWritable.class);
        job.setMapOutputValueClass(LongWritable.class);
	
	// DO NOT MODIFY THE FOLLOWING TWO LINES OF CODE:
        job.setOutputKeyClass(LongWritable.class);
        job.setOutputValueClass(LongWritable.class);
	
	// You'll want to modify the following based on what you call your
	// mapper and reducer classes for the Histogram Phase
        job.setMapperClass(HistMap.class); // currently the default Mapper
        job.setReducerClass(HistReduce.class); // currently the default Reducer
	
        job.setInputFormatClass(SequenceFileInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
	
	// By declaring i above outside of loop conditions, can use it
	// here to get last bfs output to be input to histogram
        FileInputFormat.addInputPath(job, new Path("bfs-"+ i +"-out"));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
	
        job.waitForCompletion(true);
    }

}
