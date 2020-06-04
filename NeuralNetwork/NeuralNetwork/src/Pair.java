import java.util.ArrayList;
import java.util.List;

public class Pair<T1, T2> {
	public final T1 l;
	public final T2 r;
	
	public Pair(T1 l, T2 r) {
		this.l=l;
		this.r=r;
	}
	
	public String toString() {
		return " ( "+this.l+" , "+this.r+" ) ";}
	
	public static List<Pair<?,?>> joinLists(List<Double> tl,List<?> tr){
		if(tl.size()!=tr.size())
			return null;
		List<Pair<?,?>> result=new ArrayList<Pair<?,?>>();
		for(int i=0;i<tl.size();i++)
			result.add(new Pair(tl.get(i), tr.get(i)));
		return result;
	}
}
