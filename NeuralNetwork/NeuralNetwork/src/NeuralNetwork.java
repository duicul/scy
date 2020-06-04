import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;

public class NeuralNetwork {
	//private InputLayer il=null;
	private List<Layer> layers;
	
	public NeuralNetwork() {
		this.layers=new ArrayList<Layer>();
	}
	
	public void addLayer(OutputLayer ol) {
		if(this.layers.size()>0)
			this.layers.add(ol);
	}
	
	public void addLayer(InputLayer il) {
		if(this.layers.size()==0)
			this.layers.add(il);
		else 
			this.layers.set(0, il);
	}
	
	public void addLayer(Layer l) {
		if(this.layers.size()>1 && l instanceof InputLayer) 
			return;
		if(this.layers.size()==0 && l instanceof OutputLayer) 
			return;
		
		this.layers.add(l);
	}
		
	public List<Double> forward(List<Double> inp) {
		List<Double> result = inp;
		for(Layer l:this.layers)
			result=l.apply(result);
		return result;
	}
	
	public String toString() {
		String s="";
		int ind=1;
		for(Layer l:this.layers) {
			s+="Layer "+ind+++"\n";
			s+=l+"\n";
		}
		return s;}
	
	public List<Double> train(Double lr,List<Double> inps,List<Double> target){
		List<Double> guess=this.forward(inps);
		if(guess.size()!=target.size())
			return null;
		List<Double> error=new ArrayList<Double>();
		for(int i=0;i<guess.size();i++)
			error.add(target.get(i)-guess.get(i));
		return error;
		
	}
	
}
