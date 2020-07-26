import java.util.List;

public abstract class OutputLayer extends Layer {

	public OutputLayer(int size,int prev_layer,ActivationFunction act,ErrorMeasure err) {
		super(size);
		// TODO Auto-generated constructor stub
	}

	@Override
	public abstract List<Double> apply(List<Double> inp);
	
	

}
