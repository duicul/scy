import java.lang.reflect.InvocationTargetException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class FullyConnectedLayer extends OutputLayer {

	public FullyConnectedLayer(int size,int prev_layer,ActivationFunction act,ErrorMeasure err) {
		super(size,prev_layer,act,err);
		this.lp=new ArrayList<Perceptron>();
		for(int i=0;i<size;i++)
			this.lp.add(new Perceptron(prev_layer,act,err));
	}

	@Override
	public List<Double> apply(List<Double> inp) {
		return lp.parallelStream().map(x->x.forward(inp)).collect(Collectors.toList());		
	}

	@Override
	public List<Double> train(List<Double> error) {
		
		
		// TODO Auto-generated method stub
		return null;
	}

}
