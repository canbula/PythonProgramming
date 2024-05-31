
$(document).ready(function() {
    
        $('#conn_type').change(function(){
            if ($(this).val() === 'DropBox' || $(this).val() === 'GoogleDrive'){
                $('#server, #port, #username, #passwd, #sshkey').val('').prop('disabled', true);
            } else {
                $('#server, #port, #username, #passwd, #sshkey').prop('disabled', false);
                fetchBookmarkData();
            }
        });

    $('#submitBtn').click(function() {
        var conn_type = $('#conn_type').val();
        var username = $('#username').val();
        var server = $('#server').val();
        var port = $('#port').val();
        var passwd = $('#passwd').val();
        var sshkey = $('#sshkey').val();

        if(conn_type =="DropBox" || conn_type =="GoogleDrive"){
            var data = JSON.stringify({conn_type: conn_type,
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
                    window.opener.getServersFiles();
                    window.close();
                },
                error: function(xhr, status, error) {
                    console.error('Hata:', error);
                }
            });
        }else if(conn_type =="GoogleDrive"){
            connectGoogleDrive();
            listGoogleDriveFolders();
        }else{
            if (!username || !server|| !port || !passwd) {
                if(!sshkey){
                    alert('Hata: Eksik alanlar var');
                    return; 
                }else{
                    //sshkey ile bağlan
                }
                
            }
            var data = JSON.stringify({conn_type: conn_type,
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
                    window.opener.getServersFiles();
                    window.close();
                },
                error: function(xhr, status, error) {
                    console.error('Hata:', error);
                }
            });
        }
        

        
    });
});

function fetchBookmarkData() {
    $.ajax({
        url: '/api/bookmark', // Ensure this URL is correct and accessible from the client
        type: 'GET',
        success: function(data) {
            console.log('Fetched data:', data);
            $('#conn_type').val(data.CONNECTION_TYPE); // Example connection type, map appropriately
            $('#username').val(data.USERNAME);
            $('#server').val(data.HOSTNAME);
            $('#port').val(data.PORT);
            $('#passwd').val(data.PASSWORD);
            // $('#sshkey').val(); You can set SSH key if it's part of your API response
        },
        error: function(error) {
            console.log('Error fetching data:', error);
            alert('Failed to fetch data. Check console for details.');
        }
    });
}

/*
    GOOGLE DRİVE İÇİN FONKSİYONLAR
*/
function connectGoogleDrive(){
    fetch('/google-auth-url')
        .then(response => response.json())
        .then(data => {
            // Kullanıcıyı yetkilendirme sayfasına yönlendir
            window.location.href = data.url;
        })
        .catch(error => {
            console.error('Google yetkilendirme URL alınamadı:', error);
        });
}

function listGoogleDriveFolders() {
    fetch('/list-google-drive-folders')
        .then(response => response.json())
        .then(data => {
            console.log('Google Drive Klasörleri:', data.folders);
        })
        .catch(error => {
            console.error('Google Drive klasörleri alınamadı:', error);
        });
}