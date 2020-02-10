package my.cbd01.cbd01;

import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.Set;
import redis.clients.jedis.Jedis;

public class Messenger {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Jedis jedis = new Jedis("localhost");
        String logAtual = "";
        String unlgdMsg = "\nO que deseja fazer?\n 1-Add users;\n 2-Log In\n 3-Sair";
        String lgdMsg = "\nEscolha uma açao, \n 1-Seguir Users;\n 2-Ler Mensagens\n 3-Escrever Mensagem\n 4-LogOut";
        boolean active = true;
        String USERS = "usersList";
        String RELATIONS = "-relationsHash";
        String FOLLOWING = "-following";

        while (active) {
            if (logAtual.equals("")) {
                System.out.println(unlgdMsg);
                String ans = sc.nextLine();
                switch (ans) {
                    case "1":
                        System.out.print("Insira o nome do novo user: >>");
                        String temp_user = sc.nextLine();
                        jedis.sadd(USERS, temp_user);
                        break;
                    case "2":
                        Set<String> temp_list = jedis.smembers(USERS);
                        if (temp_list.size() == 0) {
                            System.out.println("Nao ha users registados...");
                            break;
                        } else {
                            System.out.println("Diga qual dos users quer ser: ");
                            for (String s : temp_list) {
                                System.out.println(s);
                            }
                            String chosen_user = sc.nextLine();
                            if (jedis.sismember(USERS, chosen_user)) {
                                System.out.println("Entrou como " + chosen_user);
                                logAtual = chosen_user;
                            } else {
                                System.out.println("[ERRO] User nao existe!");
                            }
                        }
                        break;
                    case "3":
                        System.out.println("\n--Adeus");
                        active = false;
                        jedis.flushAll();
                        break;
                }

            } else {
                System.out.println("as [" + logAtual + "] " + lgdMsg);
                String ans = sc.nextLine();
                switch (ans) {
                    case "1":
                        System.out.println("Users que JÀ segue: ");
                        Set<String> intersected = jedis.sinter(USERS, logAtual + FOLLOWING);
                        System.out.println("in: " + intersected);

                        System.out.println("Users que NAO segue: ");
                        Set<String> diferenced = jedis.sdiff(USERS, logAtual + FOLLOWING);
                        System.out.println("dif: " + diferenced);

                        System.out.print("Seguir: >>");
                        String temp_ans = sc.nextLine();
                        if (diferenced.contains(temp_ans) && !temp_ans.equals(logAtual)) {
                            jedis.sadd(logAtual + FOLLOWING, temp_ans);
                        } else {
                            System.out.println("[ERRO] Pessoa invalida!!");
                        }
                        break;
                    case "2":
                        System.out.println("Escolha alguem para ler: ");
                        Set<String> intersected2 = jedis.sinter(USERS, logAtual + FOLLOWING);
                        System.out.println("dif: " + intersected2);
                        System.out.print(">>");
                        String temp_ans2 = sc.nextLine();
                        if (intersected2.contains(temp_ans2) && !temp_ans2.equals(logAtual)) {
                            Map<String,String> allMsg = jedis.hgetAll(temp_ans2 + RELATIONS);
                            System.out.println(allMsg);
                        } else {
                            System.out.println("[ERRO] Pessoa invalida!!");
                        }

                        break;
                    case "3":
                        System.out.print("Digite a mensagem a enviar: ");
                        String msg = sc.nextLine();
                        jedis.hset(logAtual+RELATIONS, "msg-"+jedis.hlen(logAtual+RELATIONS),msg);
                        break;
                    case "4":
                        logAtual = "";
                        break;
                }
            }

        }
    }

}
