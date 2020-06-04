
public class DifferenceError implements ErrorMeasure {
	
	private static DifferenceError sf=null;
	
	@Override
	public Double measure(double guess, double target) {
		return guess-target;
	}

	private DifferenceError() {}
	
	public static DifferenceError getIsntance() {
		if(sf==null)
			sf=new DifferenceError();
		return sf;
	}
}
