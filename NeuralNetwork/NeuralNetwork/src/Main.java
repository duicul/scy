import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

public class Main {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
			//BigDecimal bd = new BigDecimal(123456);
			//System.out.println(bd.divide(new BigDecimal(331)));
			NeuralNetwork nn=new NeuralNetwork();
			InputLayer il=new InputLayer(2);
			nn.addLayer(il);
			//nn.addLayer(4,FullyConnectedLayer.class,SigmoidFunction.class,DifferenceError.class);
			OutputLayer flc=new FullyConnectedLayer(3,2,SigmoidFunction.getIsntance(),DifferenceError.getIsntance());
			OutputLayer flc1=new FullyConnectedLayer(3,3,SigmoidFunction.getIsntance(),DifferenceError.getIsntance());
			OutputLayer flc2=new FullyConnectedLayer(3,3,SigmoidFunction.getIsntance(),DifferenceError.getIsntance());
			OutputLayer flc3=new FullyConnectedLayer(3,3,SigmoidFunction.getIsntance(),DifferenceError.getIsntance());
		
			nn.addLayer(flc);
			nn.addLayer(flc1);
			nn.addLayer(flc2);
			nn.addLayer(flc3);
			
			List<Double> inps = new ArrayList<Double>();
			inps.add(2.0);
			inps.add(3.0);
			List<Double> target= new ArrayList<Double>();
			target.add(1.0);
			target.add(1.0);
			target.add(1.0);
			//inps.add(4.0);
			System.out.println(nn);
			System.out.println(nn.train(1.0, inps, target));
			//System.out.println(flc.apply(inps));
			System.out.println(nn.forward(inps));
	}

}
