package my.cbd01.cbd01;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;
import redis.clients.jedis.Jedis;

public class AutoComplete {

    public static void main(String[] args) {
        Path p1 = Paths.get("../female-names.txt");
        List<String> nomes;
        Jedis jedis = null;
        try {

            nomes = Files.readAllLines(p1);

            jedis = new Jedis("localhost");

            //Read from the stream
            for (String nome : nomes) {//for each line of content in contents
                jedis.set(nome, "0");
//                System.out.println(nome);// print the line
            }

        } catch (IOException ex) {
            ex.printStackTrace();//handle exception here
        }

        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.print("Search for ('Enter' for quit): ");
            String ans = sc.nextLine();
            if (ans.equals("")) {
                break;
            } else {
                List<String> temp_list = new ArrayList<>();
                for (String s : jedis.keys(ans + "*")) {
                    temp_list.add(s);
                }
//                jedis.keys(ans + "*").stream().forEach(System.out::println);
                Collections.sort(temp_list);
                temp_list.stream().forEach(System.out::println);
            }
        }
        jedis.flushAll();
    }

}
