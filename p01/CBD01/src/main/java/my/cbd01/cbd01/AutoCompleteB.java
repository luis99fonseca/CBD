package my.cbd01.cbd01;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.ScanParams;
import redis.clients.jedis.ScanResult;
import redis.clients.jedis.Tuple;

public class AutoCompleteB {

    public static void main(String[] args) {
        Path p1 = Paths.get("../nomes-registados-2018.csv");
        List<String> nomes;
        Jedis jedis = null;
        try {

            nomes = Files.readAllLines(p1);

            jedis = new Jedis("localhost");

            //Read from the stream
            for (String nome : nomes) {//for each line of content in contents
                String[] data = nome.split(",");
                jedis.zadd("registredNames", Double.parseDouble(data[2]), data[0]);
            }

        } catch (IOException ex) {
            ex.printStackTrace();//handle exception here
        }

        Scanner sc = new Scanner(System.in);
        
        /*Alternative 1: loads all data, maintains ordering*/
        if (true) {
            while (true) {
                System.out.print("[A1] Search for ('Enter' for quit): ");
                String ans = sc.nextLine();
                if (ans.equals("")) {
                    break;
                } else {
                    Set<Tuple> temp_list = new LinkedHashSet<>();
                    temp_list = jedis.zrevrangeWithScores("registredNames", 0, -1);

                    int i = 0;
                    for (Tuple name : temp_list) {
                        if (name.getElement().toLowerCase().startsWith(ans.toLowerCase())) {
                            System.out.println(name);
                        }
                    }

                }
            }
        } else {
            /*Alternative 2: doesn't load all data, doesn't maintains ordering*/
            while (true) {
                System.out.print("[A2] Search for ('Enter' for quit): ");
                String ans = sc.nextLine();
                if (ans.equals("")) {
                    break;
                } else {
                    Set<Tuple> temp_list = new LinkedHashSet<>();
                    String cursor = "0";
                    ScanParams scanParams = new ScanParams();
                    scanParams.match(ans + "*");
                    while (true) {
                        ScanResult<Tuple> sr = jedis.zscan("registredNames", cursor, scanParams);
                        cursor = sr.getCursor();
                        temp_list.addAll(sr.getResult());
                        if (cursor.equals("0")) {
                            break;
                        }
                    }

                    for (Tuple name : temp_list) {
                        if (name.getElement().toLowerCase().startsWith(ans.toLowerCase())) {
                            System.out.println(name);
                        }
                    }

                }
            }
        }
        jedis.flushAll();

    }

}
