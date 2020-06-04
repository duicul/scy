import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;

public class Perceptron {

	private List<Input> inputs = new ArrayList<Input>();
	private ActivationFunction ac;
	private ErrorMeasure err;
	public Perceptron(int no_inputs,ActivationFunction activfunc,ErrorMeasure error) {
		for(int i=0;i<no_inputs;i++)
			this.inputs.add(new Input());
		this.ac=activfunc;
		this.err=error;}
	
	public Double forward(List<Double> vals) {
		//System.out.println(this.inputs);
		if(this.inputs.size()!=vals.size())
			return null;
		List<Pair<Double,Input>> lpi=new ArrayList<Pair<Double,Input>>();
		for(int i=0;i<vals.size();i++)
			lpi.add(new Pair(vals.get(i),this.inputs.get(i)));
		return lpi.parallelStream().map(x->x.r.forward(x.l)).reduce(0.0,(x,y)->x+y);}
	
	
	public String toString() {
		String s="";
		s+=this.inputs.size()+" inputs\n";
		for(Input i:inputs)
			s+=" "+i+"\n";
		return s;}
	
	public List<Double> train(Double error){
		Double weight_sum=this.inputs.parallelStream().mapToDouble(x->x.getWeight()).sum();
		List<Double> errList=new ArrayList<Double>();
		for(Input i:this.inputs) {
			errList.add(i.adjust(error*i.getWeight()/weight_sum));
		}
		return errList;
	}
	
	
}
