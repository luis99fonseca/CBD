/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ua.p02.e2_4;

import com.mongodb.BasicDBObject;
import com.mongodb.Block;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.client.AggregateIterable;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoCursor;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Accumulators;
import com.mongodb.client.model.Aggregates;
import java.time.Instant;
import java.util.Arrays;
import java.util.Date;
import org.bson.Document;
import static com.mongodb.client.model.Filters.*; //para os eq() e assim
import com.mongodb.client.model.Indexes;
import static com.mongodb.client.model.Projections.*;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

public class NewMain {

    //https://mongodb.github.io/mongo-java-driver/3.4/driver/getting-started/quick-start/
    public static void main(String[] args) {
        MongoClient mongoClient = new MongoClient("localhost", 27017);
//        mongoClient.getDatabaseNames(); //https://stackoverflow.com/a/15416618
        MongoCursor<String> dbsCursor = mongoClient.listDatabaseNames().iterator();
        System.out.println("\nBases de dados: ");
        while (dbsCursor.hasNext()) {
            System.out.print(dbsCursor.next() + "; ");
        }

        MongoDatabase db = mongoClient.getDatabase("cbd202");
        dbsCursor = db.listCollectionNames().iterator();
        System.out.println("\nColeçoes: ");
        while (dbsCursor.hasNext()) {
            System.out.print(dbsCursor.next() + "; ");
        }

        MongoCollection restC = db.getCollection("rest");
        MongoCursor<Document> cursor = restC.find().iterator();
        System.out.println("\nRest tem este nº de documentos: " + restC.count());

        System.out.print("\nSendo o Primeiro: ");
        Document myDoc = (Document) restC.find().first();
        System.out.println(myDoc.toJson());

        Instant instant = Instant.parse("2017-01-25T09:28:04.041Z");
        Date timestamp = Date.from(instant);

        //Nota: tinha um date a mais, porque isto poe automaticamente...
        Document doc = new Document("address", new Document("building", 9876)
                .append("coord", Arrays.asList(40.898989, 40.898989))
                .append("rua", "Principal")
                .append("zipcode", "10462")
        ).append("localidade", "Viseu")
                .append("gastronomia", "Tuga")
                .append("grades", Arrays.asList(new Document("date", timestamp)
                        .append("grade", "A")
                        .append("score", 2)
                )
                )
                .append("nome", "Muita Bom")
                .append("restaurant_id", "00011122");
        //restC.insertOne(doc);

        //Onde está "Bom" deve alternar-se por "Mau" (e vice-versa) a cada execução, como forma de teste
        Document mydoc = (Document) restC.find(eq("nome", "Muita Mau")).first();
        System.out.println("\nAntes: " + mydoc.toJson());

        restC.updateOne(eq("nome", "Muita Mau"), new Document("$set", new Document("nome", "Muita Bom")));

        mydoc = (Document) restC.find(eq("nome", "Muita Bom")).first();

        System.out.println("\nDepois: " + mydoc.toJson());
        //Fim de Edição

        System.out.println("\n-----------------------");
        System.out.println("\nIndexes: ");
        for (Iterator it = restC.listIndexes().iterator(); it.hasNext();) {
            Document index = (Document) it.next();
            System.out.println(index.toJson());
        }
        System.out.println("\nLOCALIDADE: ");

        long lt = System.nanoTime();
        FindIterable r1 = restC.find(eq("localidade", "Bronx"));
        System.out.println("\tsem index: " + (System.nanoTime() - lt));

        restC.createIndex(new Document("localidade", 1));
//        restC.createIndex(Indexes.ascending("localidade"));

        long lt2 = System.nanoTime();
        FindIterable r2 = restC.find(eq("localidade", "Bronx"));
        System.out.println("\tcom index: " + (System.nanoTime() - lt2));

        System.out.println("\nGASTRONOMIA: ");

        long lt5 = System.nanoTime();
        FindIterable r5 = restC.find(eq("gastronomia", "American"));
        System.out.println("\tsem index: " + (System.nanoTime() - lt5));

        restC.createIndex(new Document("gastronomia", 1));
//        restC.createIndex(Indexes.ascending("gastronomia"));

        long lt6 = System.nanoTime();
        FindIterable r6 = restC.find(eq("gastronomia", "American"));
        System.out.println("\tcom index: " + (System.nanoTime() - lt6));

        System.out.println("\nNOME: ");

        long lt3 = System.nanoTime();
        FindIterable r3 = restC.find(eq("nome", "Muita Mau"));
        System.out.println("\tsem index: " + (System.nanoTime() - lt3));

        restC.createIndex(Indexes.text("nome"));

        long lt4 = System.nanoTime();
        FindIterable r4 = restC.find(eq("nome", "Muita Mau"));
        System.out.println("\tcom index: " + (System.nanoTime() - lt4));

        System.out.println("\nIndexes Apos: ");
        for (Iterator it = restC.listIndexes().iterator(); it.hasNext();) {
            Document index = (Document) it.next();
            System.out.println(index.toJson());
        }
        restC.dropIndexes();

//        Iterator<Document> cLoc = old_countLocalidades(restC).iterator();
//        while (cLoc.hasNext()){
//            System.out.println("Numero de cidades distintas: "+ cLoc.next().getInteger("count") );
//        }
        System.out.println("\nNumero de cidades distintas: " + countLocalidades(restC));

//        Iterator<Document> rPLocalidade = old_countRestByLocalidade(restC).iterator();
        System.out.println("\nNumero de restaurantes por localidade:");
//        while (rPLocalidade.hasNext()) {
//            Document t_d = rPLocalidade.next();
//            System.out.println("-> " + t_d.getString("_id")  + " - " + t_d.getInteger("total"));
//        }
        for (Map.Entry<String, Integer> entry : countRestByLocalidade(restC).entrySet()) {
            System.out.println("-> " + entry.getKey() + " - " + entry.getValue());
        }

//        Iterator<Document> rPLocPGast = old_countRestByLocalidadeByGastronomia(restC).iterator();
        System.out.println("\nNumero de restaurantes por localidade e gastronomia:");
//        while (rPLocPGast.hasNext()) {
//            Document td = rPLocPGast.next();
//            System.out.println("-> " + td.toString());
//            Document t_d2 = (Document) td.get("_id");
//            t_d2 = (Document) t_d2.get("_id");
//            System.out.println("<<< " + t_d2.get("loc") + " - " + td.getInteger("total"));
//        }
        for (Map.Entry<String, Integer> entry : countRestByLocalidadeByGastronomia(restC).entrySet()) {
            System.out.println("-> " + entry.getKey() + " - " + entry.getValue());
        }

        String t_nome = "Park";
//        MongoCursor sName = old_getRestWithNameCloserTo(restC, t_nome).iterator();
        System.out.println("\nNome de restaurante contendo '" + t_nome + "' no nome:");
//        while (sName.hasNext()) {
//            System.out.println("-> " + sName.next().toString());
//        }
        for (String s : getRestWithNameCloserTo(restC, t_nome)) {
            System.out.println("-> " + s);
        }
    }

    public static AggregateIterable<Document> old_countLocalidades(MongoCollection mc) {
        Block<Document> printBlock = document -> System.out.println(document.toJson());
        return mc.aggregate(
                Arrays.asList(
                        Aggregates.group("$localidade", Accumulators.sum("count", 1)),
                        Aggregates.count()
                ));
    }

    public static int countLocalidades(MongoCollection mc) {
        Block<Document> printBlock = document -> System.out.println(document.toJson());
        AggregateIterable<Document> temp_doc = mc.aggregate(
                Arrays.asList(
                        Aggregates.group("$localidade", Accumulators.sum("count", 1)),
                        Aggregates.count()
                ));
        while (temp_doc.iterator().hasNext()) {
            return temp_doc.iterator().next().getInteger("count");
        }
        return 0;
    }

    public static AggregateIterable old_countRestByLocalidade(MongoCollection mc) {
        return mc.aggregate(Arrays.asList(
                Aggregates.group("$localidade", Accumulators.sum("total", 1))
        ));
    }

    public static Map<String, Integer> countRestByLocalidade(MongoCollection mc) {
        Iterator<Document> temp_doc = mc.aggregate(Arrays.asList(
                Aggregates.group("$localidade", Accumulators.sum("total", 1))
        )).iterator();
        Map<String, Integer> temp_map = new HashMap<>();
        while (temp_doc.hasNext()) {
            Document t_d = temp_doc.next();
            temp_map.put(t_d.getString("_id"), t_d.getInteger("total"));
        }
        return temp_map;
    }

    public static AggregateIterable old_countRestByLocalidadeByGastronomia(MongoCollection mc) {
        Map<String, Object> dbObjIdMap = new HashMap<String, Object>();
        dbObjIdMap.put("loc", "$localidade");
        dbObjIdMap.put("gast", "$gastronomia");
        DBObject groupFields = new BasicDBObject("_id", new BasicDBObject(dbObjIdMap));
        return mc.aggregate(Arrays.asList(
                Aggregates.group(groupFields, Accumulators.sum("total", 1))
        ));
    }

    public static Map<String, Integer> countRestByLocalidadeByGastronomia(MongoCollection mc) {
        Map<String, Integer> temp_map = new HashMap<>();

        Map<String, Object> dbObjIdMap = new HashMap<String, Object>();
        dbObjIdMap.put("loc", "$localidade");
        dbObjIdMap.put("gast", "$gastronomia");
        DBObject groupFields = new BasicDBObject("_id", new BasicDBObject(dbObjIdMap));
        Iterator<Document> temp_doc = mc.aggregate(Arrays.asList(
                Aggregates.group(groupFields, Accumulators.sum("total", 1))
        )).iterator();

        while (temp_doc.hasNext()) {
            Document td = temp_doc.next();
            Document t_d2 = (Document) td.get("_id");
            t_d2 = (Document) t_d2.get("_id");
            temp_map.put(t_d2.get("loc") + " | " + t_d2.get("gast"), td.getInteger("total"));
        }
        return temp_map;

    }

    public static FindIterable old_getRestWithNameCloserTo(MongoCollection mc, String name) {
        Pattern pattern = Pattern.compile(name, Pattern.CASE_INSENSITIVE);
        return mc.find(regex("nome", pattern)).projection(new Document("nome", 1));
    }

    public static List<String> getRestWithNameCloserTo(MongoCollection mc, String name) {
        List<String> temp_list = new ArrayList<>();

        Pattern pattern = Pattern.compile(name, Pattern.CASE_INSENSITIVE);
        Iterator<Document> temp_doc = mc.find(regex("nome", pattern)).projection(new Document("nome", 1)).iterator();

        while (temp_doc.hasNext()) {
            Document td = temp_doc.next();
            temp_list.add(td.getString("nome"));
        }
        return temp_list;
    }

}
