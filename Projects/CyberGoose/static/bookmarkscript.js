$(document).ready(function() {
    getBookMarks();
});


function getBookMarks(){
    console.log("bookmark");

    $.ajax({
        url: '/api/getBookmarksList', 
        type: 'GET',
        success: function(data) {
                var tableBody = document.getElementById('bookmark_table');
                tableBody.innerHTML = '';

                for (var i = 0; i < data.length; i++) {
                    var newRow = tableBody.insertRow();
                    var cell1 = newRow.insertCell(0);
                    var cell2 = newRow.insertCell(1);
                    var cell3 = newRow.insertCell(2);
                    var cell4 = newRow.insertCell(3);  
                    var cell5 = newRow.insertCell(4);
                    var cell6 = newRow.insertCell(5);
                    var cell7 = newRow.insertCell(6);
                    var cell8 = newRow.insertCell(7);
                    var cell9 = newRow.insertCell(8);


                    cell1.innerHTML = data[i].ID;
                    cell2.innerHTML = data[i].CONNECTION_NAME;
                    cell3.innerHTML = data[i].CONNECTION_TYPE;
                    cell4.innerHTML = data[i].HOSTNAME;
                    cell5.innerHTML = data[i].PORT;
                    cell6.innerHTML = data[i].USERNAME;
                    cell7.innerHTML = data[i].PASSWORD;
                    cell8.innerHTML = '<button type="button" class="btn btn-primary" onclick="connect(\'' + data[i].CONNECTION_TYPE + '\', \'' + data[i].HOSTNAME + '\', \'' + data[i].PORT + '\', \'' + data[i].USERNAME + '\', \'' + data[i].PASSWORD + '\')">Bağlan</button>';                
                    cell9.innerHTML = '<button type="button" class="btn btn-danger" onclick="deleteBookMark(\'' + data[i].ID + '\')"><i class="fas fa-trash-alt"></i></button>';
                }
                },error: function(xhr, status, error) {
                console.error('Hata:', error);
            }
        });
}

function connect(conn_type, server, port, username, passwd){
        var sshkey = "";
        var data = JSON.stringify({
            conn_type: conn_type,
            username: username,
            server: server,
            port: port,
            passwd: passwd,
            sshkey: sshkey});
            $.ajax({
                type: 'POST',
                url: '/submit',
                contentType: 'application/json',
                data: data,
                success: function(response) {
                console.log('Başarılı:', response);
                alert("Bağlantı Başarılı");
                window.opener.getServersFiles();
                window.close();
                },
                error: function(xhr, status, error) {
                console.error('Hata:', error);
                }
            });
}

function saveBookmark() {
    var connectionName = document.getElementById('new_connection_name').value;
    var connectionType = document.getElementById('new_connection_type').value;
    var hostname = document.getElementById('new_hostname').value;
    var port = document.getElementById('new_port').value;
    var username = document.getElementById('new_username').value;
    var password = document.getElementById('new_password').value;

    if (connectionName && connectionType && hostname && port && username && password) {
        var newBookmark = {
            CONNECTION_NAME: connectionName,
            CONNECTION_TYPE: connectionType,
            HOSTNAME: hostname,
            PORT: port,
            USERNAME: username,
            PASSWORD: password
        };

        $.ajax({
            url: '/api/saveBookmark',
            type: 'POST',
            data: JSON.stringify(newBookmark),
            contentType: 'application/json',
            success: function(response) {
                getBookMarks();
            },
            error: function(xhr, status, error) {
                console.error('Error saving bookmark:', error);
            }
        });
    } else {
        alert('Please fill in all fields.');
    }
}
function deleteBookMark(id){
    alert(id);
    $.ajax({
        url: '/api/deleteBookmark',
        type: 'POST',
        data: JSON.stringify({id: id}),
        contentType: 'application/json',
        success: function(response) {
            getBookMarks();
        },
        error: function(xhr, status, error) {
            console.error('Error deleting bookmark:', error);
        }
    });
}