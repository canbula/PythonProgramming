$(document).ready(function() {
    var urlParams = new URLSearchParams(window.location.search);
    var filepath = urlParams.get('filepath');
    getFileInfo(filepath);
    });

    function fileInfUpdate(){
        var filepath = $('#filepath').val();
        var filemod = $('#filemod').val();
        var data = JSON.stringify({filepath: filepath, filemod: filemod});

        $.ajax({
            type: 'POST',
            url: '/api/fileUpdate',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                console.log('Başarılı:', response);
                getFileInfo(filepath);
                                 
            },error: function(xhr, status, error) {
                console.error('Hata:', error);
            }
        });
    }

    function getFileInfo(filepath){
    $('#filepath').val(filepath);
    var data = JSON.stringify({filepath: filepath});
    $.ajax({
        type: 'POST',
        url: '/api/fileinfo',
        contentType: 'application/json',
        data: data,
        success: function(response) {
                console.log('Başarılı:', response);
                var data = response;
                $('#filename').val(data.FileName);
                $('#filetype').val(data.Type);
                $('#filesize').val(data.Size);
                $('#filechange').val(data.Change);
                $('#filemod').val(data.filemod);                   
            },error: function(xhr, status, error) {
                console.error('Hata:', error);
            }
        });
    }