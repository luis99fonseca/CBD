function count_prefix() {

   return db.phones.aggregate( {$group : {"_id":"$components.prefix", total: {$sum : 1 } } });
}
