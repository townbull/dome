/**
 * Created by zhu on 3/16/14.
 */

 $.ajax({
            url: "showlist",
            data: {'userId':{{ user.id }}},
            type: "POST"
        }).done(function(data){

            //var f = JSON.parse(data);
            var files = data["files"];

            var table = document.getElementById("showlist");
        for(var i=0; i<files.length; i++){
            var row = table.insertRow(1);
            var cell0 = row.insertCell(0);
            var cell1 = row.insertCell(1);
            var cell2 = row.insertCell(2);
            var cell3 = row.insertCell(3);
            var cell4 = row.insertCell(4);
           // var img = document.createElement('img');
            cell0.innerHTML=files[i].fields.source;
            cell1.innerHTML="<img src="+ files[i].fields.icon+" height='16' width='16'>";
            cell2.innerHTML="<a href="+files[i].fields.link+" target='_blank'>"+files[i].fields.name+"</a>";
            cell3.innerHTML=files[i].fields.size;
            cell4.innerHTML=files[i].fields.lastEditTime;
        }
        });
