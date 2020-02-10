/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package my.cbd01.cbd01;

import java.util.HashMap;
import java.util.Set;
import java.util.Map;
import redis.clients.jedis.Jedis;

public class SimplePost {

    private Jedis jedis;
    public static String USERS = "users"; // Key set for users' name
    public static String USERSLIST = "listed";
    public static String USERSHASH = "hashed";
    private static int counter = 0;

    public SimplePost() {
        this.jedis = new Jedis("localhost");
    }

    public void saveUser(String username) {
        jedis.sadd(USERS, username);
    }

    public Set<String> getUser() {
        return jedis.smembers(USERS);
    }

    public void saveUser(String username, String type) {
        if (type.equals("list")) {
            if (!jedis.lrange("listed", 0, -1).contains(username)) {
                jedis.lpush(USERSLIST, username);
            }
        } else if (type.equals("hash")) {
            Map<String, String> temp_map = new HashMap<>();
            temp_map.put("" + counter++, username);
            jedis.hset("PEOPLE", temp_map);
        }
    }

    public Set<String> getUser(String id) {
        return jedis.smembers(USERS);
    }

    public Set<String> getAllKeys() {
        return jedis.keys("*");
    }

    public static void main(String[] args) {
        SimplePost board = new SimplePost();
        // set some users
        String[] users = {"Ana", "Pedro", "Maria", "Luis"};
        for (String user : users) {
            board.saveUser(user);
            board.saveUser(user, "list");
            board.saveUser(user, "hash");

        }
        board.getAllKeys().stream().forEach(System.out::println);
        System.out.println("----");
        board.getUser().stream().forEach(System.out::println);

    }
}
