capicua = function () {

	lista = (db.phones.find({}, {"display":1, "_id":0}).toArray());
	var count = 0;
	lista.forEach(function(entry){
	var temp_string = JSON.stringify(entry.display).split("-")[1].split("\"")[0];
	for (var l = 0; l < temp_string.length; l++){
		if (temp_string[l] != temp_string[temp_string.length-1 - l]){
			break;
		}else if (l > (temp_string.length-1 - l)){
				/*temp_list.push(entry);*/
				print(">>> " + temp_string);
				count++;
				break;
			}
	}
	});
	print("Contagem: " + count);

	//à rafa;
    /*find_result =  (db.phones.find({}, {"display":1, "_id":0}).toArray());

    counter = 0
    for(var i = 0 ; i < find_result.length ; i++){
        number = find_result[i]['display'].split('-')[1]
        reverse_number = number.split("").reverse().join("")
        if (number == reverse_number){
            print(number)
            counter+=1
        }
    }   
    print("Total de capicuas-> "+  counter)
*/

}