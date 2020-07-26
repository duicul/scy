
public class SigmoidFunction implements ActivationFunction{
	
	private static SigmoidFunction sf=null;

	@Override
	public double activate(double val) {
		return 1/(1-Math.exp(1-val));
	}

	@Override
	public double derivate(double val) {
		return this.activate(val)*this.activate(1-val);
	}
	
	private SigmoidFunction() {}
	
	public static SigmoidFunction getIsntance() {
		if(sf==null)
			sf=new SigmoidFunction();
		return sf;
	}
	
}
