    $(document).ready(function() {
        fetchBookmarkData();
    });
    var activeFileLocal;
    var activeFileServer;
    
    function updatePath(name) {
        var path = $('#filepath').val();

        $('#filepath').val(path + '/' + name);
        getLocalFiles();
    }

    function closeConn(){
        location.reload();
    }
    function openFolderServer(name) {
        var path = $('#serverfilepath').val();
        if (name.includes(".")) {
            return;
        }
        if (path.length < 1 || path === '/') {
            $('#serverfilepath').val('/' + name);
        } else {
            // Eğer path sonu "/" ile bitiyorsa, fazladan "/" eklememek için düzeltme yapıyoruz
            if (path.endsWith('/')) {
                $('#serverfilepath').val(path + name);
            } else {
                $('#serverfilepath').val(path + '/' + name);
            }
        }
        getServersFiles();
    }
    
    
    function fileTypeControl(name) {

        if(name.includes(".txt") ||
        name.includes(".doc") ||
        name.includes(".docx") ||
        name.includes(".pdf") || 
        name.includes(".xls") || 
        name.includes(".xlsx") || 
        name.includes(".ppt") || 
        name.includes(".pptx") || 
        name.includes(".csv") || 
        name.includes(".xml") || 
        name.includes(".json") ){
            return "📄";
        }
        if(name.includes(".jpg") || name.includes(".jpeg") || name.includes(".png")){
            return "🖼️";
        }
        if(name.includes(".mp3") || name.includes(".wav") || name.includes(".flac") || name.includes(".ogg")){
            return"🎵";
        }
        if(name.includes(".mp4") || name.includes(".avi") || name.includes(".mkv") || name.includes(".mov")){
            return"🎥";
        }
        if(name.includes(".zip") || name.includes(".rar") || name.includes(".7z") || name.includes(".tar")){
            return "📦";
        }
        if(name.includes(".exe") || name.includes(".msi")){
            return"🛠️";
        }
        if(name.includes(".html") || name.includes(".css") || name.includes(".js") || name.includes(".php") || name.includes(".asp") || name.includes(".jsp")){
            return "🌐";
        }
        if(name.includes(".py")){
            return "🐍";
        }
        if(name.includes(".java")|| name.includes(".class") || name.includes(".jar")){
            return "☕";
        }
        if(name.includes(".cpp") || name.includes(".c")){
            return "🧱";
        }
        if(name.includes(".cs")){
            return "🔧";
        }if(name.includes(".sh")){
            return "📜";
        }
        return "📁";
    }

    function get(name) {
        var path = $('#filepath').val();
        $('#filepath').val(path + '/' + name);
        getLocalFiles();
    }

    function yenile(){
        getLocalFiles();
        getServersFiles();
    }

    function getServersFiles() {
        console.log("getserverfiles");
        var path = $('#serverfilepath').val();
        var data = JSON.stringify({path: path});
        $.ajax({
            type: 'POST',
            url: '/api/serverfilelist',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                    console.log('Başarılı:');
                    $('#serverfilepath').val();
                    var data = response;
                    var tableBody = document.getElementById('server_tables_body');
                    tableBody.innerHTML = '';

                    for (var i = 0; i < data.length; i++) {
                        var newRow = tableBody.insertRow();
                        var cell1 = newRow.insertCell(0);
                        var cell2 = newRow.insertCell(1);
                        var cell3 = newRow.insertCell(2);
                        var cell4 = newRow.insertCell(3);

                        newRow.ondblclick = function() {
                            var rowIndex = this.rowIndex;
                            var clickedFile = data[rowIndex -1];
                            if (clickedFile) {
                                openFolderServer(clickedFile.FileName);
                            }
                        };

                        var logo = fileTypeControl(data[i].FileName);

                        cell1.innerHTML = i + 1;
                        cell2.innerHTML = logo + " " + data[i].FileName;
                        cell3.innerHTML = data[i].TimeStamp;
                        cell4.innerHTML = data[i].Size;
    
                        

                        newRow.onclick = function(event) {
                            // Tıklanan satırı bulalım
                            var clickedRow = event.target.parentNode;
    
                            // Tüm satırlardan mavi rengini kaldıralım
                            var allRows = tableBody.getElementsByTagName("tr");
                            for (var j = 0; j < allRows.length; j++) {
                                allRows[j].classList.remove("selected-row");
                            }
    
                            // Tıklanan satıra mavi rengini ekleyelim
                            clickedRow.classList.add("selected-row");
    
                            // Tıklanan satırın indeksini alalım
                            var rowIndex = clickedRow.rowIndex;
    
                            // Seçilen satırın değerini alalım
                            activeFileServer = data[rowIndex - 1].FileName;
    
                            console.log(activeFileServer);
                        }
                    }
                },error: function(xhr, status, error) {
                    console.error('Hata:', error);
                }
            });
    }
    
    function getLocalFiles()  {
        var filepath = $('#filepath').val();
        var data = JSON.stringify({filepath: filepath});
        
        $.ajax({
            type: 'POST',
            url: '/api/localfiles',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                console.log('Başarılı:');
                var parsedArray = response;
                var tableBody = document.getElementById('files_tables_body');
                // Temizleme
                tableBody.innerHTML = '';
                for (var i = 0; i < parsedArray.length; i++) {
                    var newRow = tableBody.insertRow();
                    var cell1 = newRow.insertCell(0);
                    var cell2 = newRow.insertCell(1);
                    var cell3 = newRow.insertCell(2);
                    var cell4 = newRow.insertCell(3);

                    
                    newRow.ondblclick = function() {
                        var rowIndex = this.rowIndex;
                        var clickedFile = parsedArray[rowIndex -1];
                        if (clickedFile) {
                            updatePath(clickedFile.FileName);
                        }
                    };
                    var logo = fileTypeControl(parsedArray[i].FileName);
                    cell1.innerHTML = i + 1;
                    cell2.innerHTML = logo + " " + parsedArray[i].FileName;
                    cell3.innerHTML = parsedArray[i].TimeStamp;
                    cell4.innerHTML = parsedArray[i].Size;

                    newRow.onclick = function(event) {
                        // Tıklanan satırı bulalım
                        var clickedRow = event.target.parentNode;

                        // Tüm satırlardan mavi rengini kaldıralım
                        var allRows = tableBody.getElementsByTagName("tr");
                        for (var j = 0; j < allRows.length; j++) {
                            allRows[j].classList.remove("selected-row");
                        }

                        // Tıklanan satıra mavi rengini ekleyelim
                        clickedRow.classList.add("selected-row");

                        // Tıklanan satırın indeksini alalım
                        var rowIndex = clickedRow.rowIndex;

                        // Seçilen satırın değerini alalım
                        activeFileLocal = parsedArray[rowIndex - 1].FileName;

                        console.log(activeFileLocal);
                    }
                }
                
            },
            error: function(xhr, status, error) {
                console.error('Hata:', error);
            }
        });
        
    }

    function serverConnFunc() {
        var formURL = "serverconnection.html";
        var win = window.open(formURL, "_blank", "resizable=yes,width=600,height=600");
    }

    function uploadFile() {
        var fileName = activeFileLocal;
        var folderPath = $('#filepath').val();
        var serverpath = $('#serverfilepath').val();
        console.log("file",fileName);
        console.log("folderpath",folderPath);
        console.log("serverpath",serverpath);
        var data = JSON.stringify({fileName: fileName,
                                    folderPath: folderPath,
                                    serverpath: serverpath
                                });
        $.ajax({
            type: 'POST',
            url: '/api/uploadFile',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                    alert('Dosya başarıyla yüklendi');
                    console.log('Başarılı:',response);
                    openFolderServer("");
                },error: function(xhr, status, error) {
                    alert('Dosya yüklenirken hata oluştu');
                    console.error('Hata:', error);
                }
            });
    }
   
    function downloadFile() {
        var fileName = activeFileServer;
        var folderPath = $('#filepath').val();
        var serverpath = $('#serverfilepath').val();
        console.log("file",fileName);
        console.log("folderpath",folderPath);
        console.log("serverpath",serverpath);
        var data = JSON.stringify({fileName: fileName,
                                    folderPath: folderPath,
                                    serverpath: serverpath
                                });
        $.ajax({
            type: 'POST',
            url: '/api/downloadFile',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                alert('Dosya başarıyla indirildi');
                    console.log('Başarılı:',response);
                    getLocalFiles();
                },error: function(xhr, status, error) {
                    alert('Dosya indirilirken hata oluştu');
                    console.error('Hata:', error);
                }
            });
    }

    function deleteFileFromServer() {
        var fileName = activeFileServer;
        var serverpath = $('#serverfilepath').val();
        console.log("file",fileName);
        console.log("serverpath",serverpath);
        var data = JSON.stringify({fileName: fileName,
                                    serverpath: serverpath
                                });
        $.ajax({
            type: 'POST',
            url: '/api/deleteFileFromServer',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                    alert('Dosya başarıyla silindi');
                    console.log('Başarılı:',response);
                    openFolderServer("");
                },error: function(xhr, status, error) {
                    console.error('Hata:', error);
                }
            });
    }

    function deleteFileFromLocal() {
        var fileName = activeFileLocal;
        var folderPath = $('#filepath').val();
        console.log("file",fileName);
        console.log("folderpath",folderPath);
        var data = JSON.stringify({fileName: fileName,
                                    folderPath: folderPath
                                });
        $.ajax({
            type: 'POST',
            url: '/api/deleteFileFromLocal',
            contentType: 'application/json',
            data: data,
            success: function(response) {
                    alert('Dosya başarıyla silindi');
                    console.log('Başarılı:',response);
                    getLocalFiles();
                },error: function(xhr, status, error) {
                    console.error('Hata:', error);
                }
            });
    }
    
    function fileInfOpen() {
        var filepath1=$('#serverfilepath').val() +'/' + activeFileServer;
        var formURL = "file_inf.html";
        var win = window.open(formURL + "?filepath=" + encodeURIComponent(filepath1), "_blank", "resizable=yes,width=550,height=500");
    }
   
    function turnBackLocal(){
        var path = $('#filepath').val();
        var newPath = path.split("/");
        newPath.pop();
        $('#filepath').val(newPath.join("/"));
        getLocalFiles();

    }

    function turnBackServer(){
        var path = $('#serverfilepath').val();
        var newPath = path.split("/");
        newPath.pop();
        $('#serverfilepath').val(newPath.join("/"));
        getServersFiles();
    }

    function fetchBookmarkData() {
        $.ajax({
            url: '/api/localBookmark', // Ensure this URL is correct and accessible from the client
            type: 'GET',
            success: function(data) {
                console.log('Fetched data:', data);
                $('#filepath').val(data.PATH); 
                getLocalFiles();
                // $('#sshkey').val(); You can set SSH key if it's part of your API response
            },
            error: function(error) {
                console.log('Error fetching data:', error);
                alert('Failed to fetch data. Check console for details.');
            }
        });
    }
    
    function openBookMarksList(){
        var formURL = "bookmarks.html";
        var win = window.open(formURL, "_blank", "resizable=yes,width=1250,height=600");
    }
        
        

    