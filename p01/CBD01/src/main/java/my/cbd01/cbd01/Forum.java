
package my.cbd01.cbd01;
import redis.clients.jedis.Jedis;

public class Forum {

    private Jedis jedis;

    public Forum() {
        this.jedis = new Jedis("localhost");
        System.out.println(jedis.info());
    }

    public static void main(String[] args) {
        Forum f1 = new Forum();
        
    }
}