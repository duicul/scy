import java.util.ArrayList;
import java.util.List;

public abstract class Layer {
	protected List<Perceptron> lp;
	public Layer(int size) {
	}
	public abstract List<Double> apply(List<Double> inp);
	public String toString() {
		String s="";
		if(lp==null)
			return "no perpceptrons";
		s+=this.lp.size()+" perceptrons\n";
		for(Perceptron p:lp)
			s+=" "+p+"\n";
		return s;
	}
	
	public int size() {
		return lp==null?0:this.lp.size();
	}
	
	public abstract List<Double> train(List<Double> error);
}
