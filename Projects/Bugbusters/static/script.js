// Database Structure Buton
const dbStructure = document.getElementById("dbStructure");

//buttons
const removeButton = document.getElementById("removeBButton");
const moveTopButton = document.getElementById("moveTButton");
const moveUpButton = document.getElementById("moveUButton");
const moveDownButton = document.getElementById("moveDButton");
const moveBottomButton = document.getElementById("moveBButton");
const filePath = document.getElementById("filePath").value;
const fileName = document.getElementById("fileName").value;
const modalButton = document.getElementById("modalButton");
const spButton = document.getElementById("save-project");
const adButton = document.getElementById("ad-database");
const cButton = document.getElementById("c-database");
const fad = document.querySelector(".ddia>a#f-ad");
const fcd = document.querySelector("#f-cd");
const fsp = document.querySelector(".ddia>a#f-sp");
const fspa = document.querySelector(".ddia>a#f-spa");
const fsa = document.querySelector(".ddia>a#f-sa");
const mCT = document.getElementById("mCT");
const mCI = document.getElementById("mCI");
const openProject = document.getElementById("openProject");
const saveProject = document.getElementById("save-project");
const adDatabase = document.getElementById("ad-database");
const createTable = document.getElementById("createTable");
const modifyTable = document.getElementById("modifyTable");
const deleteTable = document.getElementById("deleteTable");
const openDataB = document.getElementById("f-open-db");
const openDatabase = document.getElementById("openDB");
const closeFileDB = document.getElementById("f-cd");
const closeDB = document.getElementById("c-database");
const fileInput = document.getElementById("formFile");
const compactDB = document.getElementById("t-cd");
const loadE = document.getElementById("t-le");
const integrityCheck = document.getElementById("t-ic");
const quickIntegrityCheck = document.getElementById("t-qic");
const fkCheck = document.getElementById("t-fkc");
const optimize = document.getElementById("t-o");
const csvFile = document.getElementById("csvFile");
const cancelFile = document.getElementById("cancelFile");
const cancelButton = document.getElementById("sqlQueryCancel");
const csv = document.getElementById("csv");
const ucsv = document.getElementById("uploadCSV");
const csvOK = document.getElementById("csvOK");
const tableToCSV = document.getElementById("tableToCSV");
const tableToJSON = document.getElementById("tableToJSON");

dbStructure.addEventListener("click", () => {
  const text = dbStructure.textContent;
  console.log(text);
});

// Browse Data Buton
const browseDataButton = document.getElementById("browseData");

browseDataButton.addEventListener("click", async () => {
  fetch("/show_table")
    .then((response) => response.json())
    .then((data) => {
      if (data.tables) {
        const tableData = data.tables;
        const genisEkran = document.querySelector(".genisEkran");
        genisEkran.innerHTML = "";

        for (const tableName in tableData) {
          const columns = tableData[tableName].columns;
          const rows = tableData[tableName].data;

          // Create table element with Bootstrap classes
          const table = document.createElement("table");
          table.classList.add("table", "table-striped", "table-bordered");
          const thead = document.createElement("thead");
          const tbody = document.createElement("tbody");

          // Create table header with search boxes
          const headerRow = document.createElement("tr");
          const searchRow = document.createElement("tr");

          columns.forEach((column) => {
            const th = document.createElement("th");
            th.textContent = column;
            headerRow.appendChild(th);

            const searchTh = document.createElement("th");
            const searchInput = document.createElement("input");
            searchInput.type = "text";
            searchInput.placeholder = `Search ${column}`;
            searchInput.setAttribute("data-column", column);
            searchInput.addEventListener("input", function () {
              filterTable(table, column, this.value);
            });
            searchTh.appendChild(searchInput);
            searchRow.appendChild(searchTh);
          });

          thead.appendChild(headerRow);
          thead.appendChild(searchRow);

          // Create table body
          rows.forEach((row) => {
            const tr = document.createElement("tr");
            row.forEach((cell) => {
              const td = document.createElement("td");
              td.textContent = cell;
              tr.appendChild(td);
            });
            tbody.appendChild(tr);
          });

          table.appendChild(thead);
          table.appendChild(tbody);
          genisEkran.appendChild(table);
        }
      }
    })
    .catch((error) => console.error("Error:", error));
});

function filterTable(table, column, query) {
  const rows = table.getElementsByTagName("tr");
  const headerCells = rows[0].getElementsByTagName("th");
  let columnIndex;

  for (let i = 0; i < headerCells.length; i++) {
    if (headerCells[i].textContent === column) {
      columnIndex = i;
      break;
    }
  }

  for (let i = 2; i < rows.length; i++) {
    // start from 2 to skip header and search rows
    const cells = rows[i].getElementsByTagName("td");
    if (
      cells[columnIndex].textContent.toLowerCase().includes(query.toLowerCase())
    ) {
      rows[i].style.display = "";
    } else {
      rows[i].style.display = "none";
    }
  }
}

// edit Paragmas Buton
const editParagmas = document.getElementById("editParagmas");

editParagmas.addEventListener("click", () => {
  const text = editParagmas.textContent;
  console.log(text);
});

// execute SQL  Buton
const executeSQL = document.getElementById("executeSQL");

executeSQL.addEventListener("click", () => {
  const genisEkranDiv = document.querySelector(".row.genisEkran");
  genisEkranDiv.innerHTML = "";

  const col = document.createElement("div");
  col.classList.add("col");

  const icons = document.createElement("div");
  icons.classList.add("row", "align-items-center");
  icons.style.height = "30px";
  icons.style.display = "flex";
  icons.style.marginBottom = "8px";

  const button1 = document.createElement("button");
  button1.classList.add("btn");
  button1.type = "button";
  button1.classList.add("execute-sql-buttons");
  const img1 = document.createElement("img");
  img1.src = "../static/icons/tab_add.svg"; // İlk ikonun resmi yolu
  img1.style.width = "100%";
  button1.appendChild(img1);
  icons.appendChild(button1);
  const button2 = document.createElement("button");
  button2.classList.add("btn");
  button2.type = "button";
  button2.classList.add("execute-sql-buttons");
  const iconClass2 = ["fa-regular", "fa-file", "fa-xs"];
  const iconColor = "#0b3275";
  const iconElement = document.createElement("i");
  iconClass2.forEach((cls) => iconElement.classList.add(cls));
  iconElement.style.color = iconColor;
  button2.appendChild(iconElement);
  icons.appendChild(button2);
  const button3 = document.createElement("button");
  button3.classList.add("btn");
  button3.type = "button";
  button3.classList.add("execute-sql-buttons");
  const img3 = document.createElement("img");
  img3.src = "../static/icons/page_save.svg"; // İlk ikonun resmi yolu
  img3.style.width = "100%";
  button3.appendChild(img3);
  icons.appendChild(button3);
  const button4 = document.createElement("button");
  button4.classList.add("btn");
  button4.type = "button";
  button4.classList.add("execute-sql-buttons");
  const img4 = document.createElement("img");
  img4.src = "../static/icons/printer.svg"; // İlk ikonun resmi yolu
  img4.style.width = "100%";
  button4.appendChild(img4);
  icons.appendChild(button4);
  const button5 = document.createElement("button");
  button5.classList.add("btn");
  button5.type = "button";
  button5.classList.add("execute-sql-buttons");
  button5.classList.add("disabled");
  button5.id = "executeSQLB";
  const img5 = document.createElement("img");
  img5.src = "../static/icons/resultset_next.svg"; // İlk ikonun resmi yolu
  img5.style.width = "100%";
  button5.appendChild(img5);
  icons.appendChild(button5);
  const button6 = document.createElement("button");
  button6.classList.add("btn");
  button6.type = "button";
  button6.id = "executeCurrent";
  button6.classList.add("execute-sql-buttons");
  button6.classList.add("disabled");
  const img6 = document.createElement("img");
  img6.src = "../static/icons/resultset_last.svg"; // İlk ikonun resmi yolu
  img6.style.width = "100%";
  button6.appendChild(img6);
  icons.appendChild(button6);
  const button7 = document.createElement("button");
  button7.classList.add("btn");
  button7.type = "button";
  button7.classList.add("execute-sql-buttons");
  button7.classList.add("disabled");
  button7.id = "stopSQL";
  const img7 = document.createElement("img");
  img7.src = "../static/icons/cancel.svg"; // İlk ikonun resmi yolu
  img7.style.width = "100%";
  button7.appendChild(img7);
  icons.appendChild(button7);
  const button8 = document.createElement("button");
  button8.classList.add("btn");
  button8.type = "button";
  button8.classList.add("execute-sql-buttons");
  button8.classList.add("disabled");
  button8.id = "saveResult";
  const img8 = document.createElement("img");
  img8.src = "../static/icons/table_save.svg"; // İlk ikonun resmi yolu
  img8.style.width = "100%";
  button8.appendChild(img8);
  icons.appendChild(button8);
  const button9 = document.createElement("button");
  button9.classList.add("btn");
  button9.type = "button";
  button9.classList.add("execute-sql-buttons");
  const img9 = document.createElement("img");
  img9.src = "../static/icons/page_find.svg"; // İlk ikonun resmi yolu
  img9.style.width = "100%";
  button9.appendChild(img9);
  icons.appendChild(button9);
  const button10 = document.createElement("button");
  button10.classList.add("btn");
  button10.type = "button";
  button10.classList.add("execute-sql-buttons");
  const iconClass10 = ["fa-solid", "fa-spell-check", "fa-xs"];
  const iconColor10 = "#3960a2";
  const iconElement10 = document.createElement("i");
  iconClass10.forEach((cls) => iconElement10.classList.add(cls));
  iconElement10.style.color = iconColor10;
  button10.appendChild(iconElement10);
  icons.appendChild(button10);
  const button11 = document.createElement("button");
  button11.classList.add("btn");
  button11.type = "button";
  button11.classList.add("execute-sql-buttons");
  const iconClass11 = ["fa-solid", "fa-indent", "fa-xs"];
  const iconColor11 = "#03682a";
  const iconElement11 = document.createElement("i");
  iconClass11.forEach((cls) => iconElement11.classList.add(cls));
  iconElement11.style.color = iconColor11;
  button11.appendChild(iconElement11);
  icons.appendChild(button11);

  col.appendChild(icons);

  const sqlQ = document.createElement("div");
  sqlQ.classList.add("sqlQ");
  const sqlQ_main = document.createElement("div");
  sqlQ_main.classList.add("sqlQ_main");
  const sqlQ_body = document.createElement("div");
  sqlQ_body.classList.add("sqlQ_body");
  const queryBox = document.createElement("div");
  const classnames = ["queryBox", "btn"];
  classnames.forEach((cls) => queryBox.classList.add(cls));
  queryBox.textContent = "Query 1";
  queryBox.classList.toggle("active");
  sqlQ_main.appendChild(queryBox);
  sqlQ_main.appendChild(sqlQ_body);
  col.appendChild(sqlQ);

  // col1 ve col2 içerisine inner1 ve inner2 div ekle
  const inner1 = document.createElement("div");
  inner1.classList.add("inner-box-left");
  // Yeni bir satır div oluştur ve içeriğine "1" yaz
  const rowDiv = document.createElement("div");
  rowDiv.textContent = "1";
  rowDiv.classList.add("row-item"); // Satır gibi davranması için bir sınıf ekleyin (CSS ile stil verebilirsiniz)
  inner1.appendChild(rowDiv);

  const inner2 = document.createElement("div");
  inner2.classList.add("inner-box-right");
  const textarea = document.createElement("textarea");
  textarea.style.width = "100%"; // Genişlik ayarı
  textarea.style.height = "-webkit-fill-available"; // Yükseklik ayarı
  textarea.id = "sql-textarea";
  inner2.appendChild(textarea);

  sqlQ_body.appendChild(inner1);
  sqlQ_body.appendChild(inner2);

  sqlQ_main.appendChild(sqlQ_body);

  // Ana col'a sqlQ_main'i ekle
  sqlQ.appendChild(sqlQ_main);

  // Geniş Ekran div'ine ana col'u ekle
  genisEkranDiv.appendChild(col);
  const sqlText = document.getElementById("sql-textarea");

  let counter = 2; // Sayacı dışarıda tanımlıyoruz, böylece her olay tetiklendiğinde sıfırlanmaz

  sqlText.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      const newRow = document.createElement("div");
      newRow.classList.add("row-item");
      newRow.style.overflowY = "auto  ";
      newRow.textContent = counter;
      inner1.appendChild(newRow);
      counter++;
    } else if (event.key === "Backspace") {
      // Backspace tuşuna basıldığında gerçekleşecek işlemler
      const cursorPosition = sqlText.selectionStart;

      // Metin alanının başında değilse ve mevcut satır boşsa
      if (
        cursorPosition !== 0 &&
        sqlText.value.charAt(cursorPosition - 1) === "\n"
      ) {
        // İlgili satırı sil
        const lines = sqlText.value.split("\n");
        const lineIndex =
          sqlText.value.substr(0, cursorPosition).split("\n").length - 1;

        if (lines[lineIndex].trim() === "") {
          // Satırda hiç karakter yoksa, row-item'ı sil
          const rowItems = inner1.querySelectorAll(".row-item");
          if (rowItems.length > 0) {
            inner1.removeChild(rowItems[rowItems.length - 1]);
          }
          counter--;
        }
      }
    }
  });
  if (dbOpened) {
    const executeSQLButton = document.getElementById("executeSQLB");
    executeSQLButton.classList.remove("disabled");
    const executeCurrentButton = document.getElementById("executeCurrent");
    executeCurrentButton.classList.remove("disabled");
    const stopSQLButton = document.getElementById("stopSQL");
    stopSQLButton.classList.remove("disabled");
    const saveResultButton = document.getElementById("saveResult");
    saveResultButton.classList.remove("disabled");
    executeSQLB.addEventListener("click", async () => {
      const sqlQuery = document.getElementById("sql-textarea").value;
      try {
        const response = await fetch("/execute_sql", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ sql_query: sqlQuery }),
        });

        const result = await response.json();
        if (response.ok) {
          const columnNames = result.data.column_names;
          const sqlResults = result.data.result;
          console.log("Column names:", columnNames);
          console.log("Result:", sqlResults);

          // Tablo öğesini oluşturun
          const table = document.createElement("table");
          table.classList.add("table");

          // Tablonun başlığını oluşturun
          const tableHead = document.createElement("thead");
          const headRow = document.createElement("tr");

          // Satır numarası için başlık oluşturun
          const thRowNum = document.createElement("th");
          thRowNum.setAttribute("scope", "col");
          thRowNum.textContent = "#";
          headRow.appendChild(thRowNum);

          // Attribute başlıklarını oluşturun
          columnNames.forEach((columnName, index) => {
            const th = document.createElement("th");
            th.setAttribute("scope", "col");
            th.textContent = columnName;
            headRow.appendChild(th);
          });

          tableHead.appendChild(headRow);
          table.appendChild(tableHead);

          // Tablonun gövdesini oluşturun
          const tableBody = document.createElement("tbody");

          // SQL sonuçlarını tabloya ekleyin
          sqlResults.forEach((row, index) => {
            const tr = document.createElement("tr");

            // Satır numarasını ekle
            const thRowIndex = document.createElement("th");
            thRowIndex.setAttribute("scope", "row");
            thRowIndex.textContent = index + 1;
            tr.appendChild(thRowIndex);

            // Her bir attribute için bir td oluşturun
            row.forEach((item) => {
              const td = document.createElement("td");
              td.textContent = item;
              tr.appendChild(td);
            });

            tableBody.appendChild(tr);
          });

          table.appendChild(tableBody);

          // Önceki sonuçları temizleyin
          const sqlQM = document.querySelector(".sqlQ_main");
          const previousResults = sqlQM.querySelectorAll(".sqlQ_result");
          previousResults.forEach((result) => {
            result.remove();
          });

          // Yeni sonuçları sayfaya ekleyin
          const sqlQResult = document.createElement("div");
          sqlQResult.classList.add("sqlQ_result");
          sqlQResult.appendChild(table);
          sqlQM.appendChild(sqlQResult);

          if (dbOpened) {
            const executeSQLButton = document.getElementById("executeSQLB");
            executeSQLButton.classList.remove("disabled");
            const executeCurrentButton =
              document.getElementById("executeCurrent");
            executeCurrentButton.classList.remove("disabled");
            const stopSQLButton = document.getElementById("stopSQL");
            stopSQLButton.classList.remove("disabled");
            const saveResultButton = document.getElementById("saveResult");
            saveResultButton.classList.remove("disabled");
          }
        } else {
          alert(result.error || result.message);
        }
      } catch (error) {
        console.error(
          "An error occurred while executing the SQL query:",
          error
        );
      }
    });
  }
});

document.addEventListener("DOMContentLoaded", function () {
  // "cog" sınıfına sahip div'i seç
  const cogDiv = document.querySelector(".cog");

  // Tıklanan resmin görünürlüğünü değiştiren bir olay dinleyici ekle
  cogDiv.addEventListener("click", function (event) {
    // Tıklanan öğe bir resim mi kontrol et
    if (event.target.tagName === "IMG") {
      // Tıklanan resmin görünürlüğünü değiştir
      event.target.classList.toggle("hidden");

      // Diğer resmin görünürlüğünü değiştir
      const otherImage = event.target.nextElementSibling;
      if (otherImage) {
        otherImage.classList.toggle("hidden");
      } else {
        // Diğer resim yoksa (yani son resim görüntüleniyorsa), ilk resmi görünür yap
        const firstImage = event.target.previousElementSibling;
        if (firstImage) {
          firstImage.classList.remove("hidden");
        }
      }
    }
  });
});

// Remote daki buttonlar için
document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".btn-group .menu-btn");

  buttons[0].classList.add("active");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      buttons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".btn-group .menu-btns");

  buttons[0].classList.add("active");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      buttons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

function openFileInput() {
  document.getElementById("fileInput").click();
}

document.getElementById("dbbutton").addEventListener("click", () => {
  const fileNewDBBut = document.getElementById("fileNewDB");
  fileNewDBBut.click();
});

document.getElementById("fileNewDB").addEventListener("click", async () => {
  const response = await fetch("/fileinfo");
  const data = await response.json();
  document.getElementById("filePath").value = data.file_path;
});

// file-new-db div tıklanıldığında fileNewDB butonunu tıklat
document.getElementById("file-new-db").addEventListener("click", () => {
  const fileNewDBBut = document.getElementById("fileNewDB");
  fileNewDBBut.click();
});
// backendden database klasörünün konumunu döndürür.
document.getElementById("fileNewDB").addEventListener("click", async () => {
  const response = await fetch("/fileinfo");
  const data = await response.json();
  document.getElementById("filePath").value = data.file_path;
});

// modaldan dosya adı girilip save a basılırsa bu bilgiler backend e gönderilir. 2. Modal açılır.
document.getElementById("saveFile").addEventListener("click", async () => {
  try {
    const filePath = document.getElementById("filePath").value;
    const fileName = document.getElementById("fileName").value;
    const response = await fetch("/save", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ file_path: filePath, file_name: fileName }),
    });

    const result = await response.json();
    console.log(result);
    if (response.ok) {
      spButton.disabled = false;
      adButton.disabled = false;
      cButton.disabled = false;
      mCT.disabled = false;
      mCI.disabled = false;
      fad.classList.remove("disabled");
      fcd.classList.remove("disabled");
      fsp.classList.remove("disabled");
      fspa.classList.remove("disabled");
      fsa.classList.remove("disabled");
      createTable.classList.remove("disabled");
      modifyTable.classList.remove("disabled");
      deleteTable.classList.remove("disabled");
      modalButton.click();
      mainWindow(result);
      executeSQLB.classList.remove("disabled");
    } else {
      console.log(result.error || result.message); // Hata mesajını ekrana basıyoruz
    }
  } catch (error) {
    console.log("An error occurred:", error);
  }
});

// Dosya adı giriş alanını seçin
const fileNameInput = document.getElementById("fileName");

// Save butonunu seçin
const saveButton = document.getElementById("saveFile");

// Dosya adı giriş alanında bir tuşa basıldığında bu fonksiyonu çalıştırın
fileNameInput.addEventListener("keyup", function () {
  // Dosya adı giriş alanının değerini alın
  const fileNameValue = fileNameInput.value.trim();

  // Dosya adı giriş alanı boş değilse veya sadece boşluklardan oluşmuyorsa
  if (fileNameValue) {
    // Save butonundaki disabled sınıfını kaldırın
    saveButton.classList.remove("disabled");
  } else {
    // Dosya adı giriş alanı boşsa veya sadece boşluklardan oluşuyorsa
    // Save butonuna disabled sınıfını ekleyin
    saveButton.classList.add("disabled");
  }
});

// Modal içindeki butonlar için
document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".tfac");

  buttons[0].classList.add("active");

  buttons.forEach((button) => {
    button.addEventListener("click", function () {
      buttons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

// Butonun devre dışı olup olmadığını kontrol eden fonksiyon
function toggleButtonCursor() {
  //divs
  const removeButton = document.getElementById("removeButton");
  const moveTopButton = document.getElementById("moveTopButton");
  const moveUpButton = document.getElementById("moveUpButton");
  const moveDownButton = document.getElementById("moveDownButton");
  const moveBottomButton = document.getElementById("moveBottomButton");

  if (
    removeButton.classList.contains("disabled") ||
    moveTopButton.classList.contains("disabled") ||
    moveUpButton.classList.contains("disabled") ||
    moveDownButton.classList.contains("disabled") ||
    moveBottomButton.classList.contains("disabled")
  ) {
    removeButton.style.cursor = "default";
    moveTopButton.style.cursor = "default";
    moveUpButton.style.cursor = "default";
    moveDownButton.style.cursor = "default";
    moveBottomButton.style.cursor = "default";
  } else {
    removeButton.style.cursor = "pointer";
    moveTopButton.style.cursor = "pointer";
    moveUpButton.style.cursor = "pointer";
    moveDownButton.style.cursor = "pointer";
    moveBottomButton.style.cursor = "pointer";
  }
}

// Sayfa yüklendiğinde ve buton durumu değiştiğinde çağrılır
document.addEventListener("DOMContentLoaded", function () {
  toggleButtonCursor();
});

// Modalda tablo oluştur butonuna tıklandığında
class QueryDivManager {
  constructor() {
    this.fieldCounter = 1;
    this.selectedRow = null;
    this.addButtonClickListener();
    this.removeButtonClickListener();
    this.setupTableNameListener();
    this.updateOkButtonState();
    this.updateSQLColumnNumbers();
    this.removeLastAddedRow();
    this.sqlQuerySaveSend();
    this.clearModal();
  }

  addButtonClickListener() {
    const addBtn = document.querySelector("#addButton");
    addBtn.addEventListener("click", () => {
      document.querySelector(".sql-fields").style.marginTop = "0";
      this.addRow();
      this.updateSQLQuery();
    });
  }

  removeButtonClickListener() {
    const removeButton = document.getElementById("removeBButton");
    removeButton.addEventListener("click", () => this.removeSelectedRow());
  }

  setupTableNameListener() {
    const tableNameInput = document.getElementById("table-name");
    tableNameInput.addEventListener("keyup", () => {
      this.updateSQLTable();
    });
  }

  setupCheckboxListeners() {
    const checkboxes = document.querySelectorAll(".checkbox");
    checkboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        this.updateSQLQuery();
      });
    });
  }

  sqlQuerySaveSend() {
    const sqlQuerySave = document.getElementById("sqlQuerySave");
    sqlQuerySave.addEventListener("click", async () => {
      this.sqlQuerySave();
      // const cancelButton = document.getElementById("sqlQueryCancel");
      cancelButton.click();
      this.clearModal();
    });
  }
  clearModal() {
    const cancelButton = document.getElementById("sqlQueryCancel");
    cancelButton.addEventListener("click", () => {
      csv.classList.remove("disabled");
      const tableNameInput = document.getElementById("table-name");
      tableNameInput.value = "";
      const databaseschema = document.getElementById("databaseschema");
      databaseschema.selectedIndex = 0;
      const withoutRowid = document.getElementById("withoutRowid");
      withoutRowid.checked = false;
      const tableName = document.getElementById("tableName");
      tableName.textContent = "";
      const fieldList = document.getElementById("fieldList");
      fieldList.innerHTML = "";
      const jsrow = document.querySelectorAll(".js-row");
      jsrow.forEach((row) => {
        row.remove();
      });
    });
  }

  addRow() {
    const newRow = document.createElement("div");
    newRow.classList.add("row", "d-flex", "js-row");

    newRow.innerHTML = `
          <div class="sql-col-name sql-col-mt"><input type="text" value="Field${this
            .fieldCounter++}"></div>
          <div class="sql-col-type sql-col-mt">
              <select class="form-select field-type" style="width:130px; position:relative; left:7px; padding:0px !important;">
                  <option selected>INTEGER</option>
                  <option value="1">TEXT</option>
                  <option value="2">BLOB</option>
                  <option value="3">REAL</option>
                  <option value="4">NUMERIC</option>
              </select>
          </div>
          <div class="sql-col-checkbox field-nullable sql-col-mt" style="left: 86px;"><input class="form-check-input" type="checkbox"></div>
          <div class="sql-col-checkbox field-primary-key sql-col-mt" style="left: 86px;"><input class="form-check-input" type="checkbox"></div>
          <div class="sql-col-checkbox field-auto-increment sql-col-mt" style="left: 86px;"><input class="form-check-input" type="checkbox"></div>
          <div class="sql-col-checkbox field-unique sql-col-mt" style="left: 80px;"><input class="form-check-input" type="checkbox"></div>
          <div class="sql-col-default field-default sql-col-mt"></div>
          <div class="sql-col-check field-check sql-col-mt""></div>
          <div class="sql-col-collation sql-col-mt">
            <select class="form-select field-collation" style="width:130px; position:relative; left:7px; padding:0px !important;">
              <option selected></option>
              <option value="1">BINARY</option>
              <option value="2">NOCASE</option>
              <option value="3">RTRIM</option>
              <option value="4">UTF16</option>
              <option value="5">UTF16CI</option>
            </select>
          </div>
          <div class="sql-col-fk field-fk sql-col-mt""></div>
      `;

    newRow.addEventListener("click", () => this.rowClickHandler(newRow));
    newRow.querySelectorAll(".field-type").forEach((select) => {
      select.addEventListener("change", () => this.updateSQLQuery());
    });
    newRow.querySelectorAll("input[type='text']").forEach((input) => {
      input.addEventListener("keyup", () => this.updateSQLQuery());
    });
    // newRow.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
    //   checkbox.addEventListener("change", () => this.updateSQLQuery());
    // });
    newRow.querySelectorAll("input[type='checkbox']").forEach((checkbox) => {
      checkbox.addEventListener("change", (event) => {
        this.handleCheckboxChange(event);
      });
    });

    document.querySelector(".queryDiv .row:last-child").after(newRow);
    this.updateOkButtonState();
    this.updateSQLColumnNumbers();
  }

  handleCheckboxChange(event) {
    const checkbox = event.target;
    const row = checkbox.closest(".row");
    const primaryKeyCheckbox = row.querySelector(".field-primary-key input");
    const autoIncrementCheckbox = row.querySelector(
      ".field-auto-increment input"
    );

    if (checkbox === autoIncrementCheckbox && checkbox.checked) {
      primaryKeyCheckbox.checked = true;
    }

    if (checkbox === primaryKeyCheckbox && !checkbox.checked) {
      autoIncrementCheckbox.checked = false;
    }

    this.updateSQLQuery();
  }
  rowClickHandler(row) {
    if (this.selectedRow !== null) {
      this.selectedRow.style.backgroundColor = "";
    }
    this.selectedRow = row;
    this.selectedRow.style.backgroundColor = "orange";
    this.updateButtonStates();
  }

  updateButtonStates() {
    const rows = document.querySelectorAll(".queryDiv .js-row");
    const totalRows = rows.length;

    // Determine the clicked row index
    const clickedRowIndex = Array.from(rows).indexOf(this.selectedRow);

    // Disable all buttons
    removeButton.classList.add("disabled");
    moveTopButton.classList.add("disabled");
    moveUpButton.classList.add("disabled");
    moveDownButton.classList.add("disabled");
    moveBottomButton.classList.add("disabled");

    // Eğer toplam satır sayısı 0 ise removeButton'u devre dışı bırak
    if (totalRows === 1) {
      removeButton.classList.remove("disabled");
      return;
    } else if (totalRows === 2) {
      // Two rows: special handling for first and second rows
      if (clickedRowIndex === 0) {
        moveDownButton.classList.remove("disabled");
        moveBottomButton.classList.remove("disabled");
        removeButton.classList.remove("disabled");
      } else if (clickedRowIndex === 1) {
        moveUpButton.classList.remove("disabled");
        moveTopButton.classList.remove("disabled");
        removeButton.classList.remove("disabled");
      }
    } else if (totalRows === 0) {
      removeButton.classList.add("disabled");
      moveBottomButton.classList.add("disabled");
      moveDownButton.classList.add("disabled");
      moveUpButton.classList.add("disabled");
      moveTopButton.classList.add("disabled");
    } else {
      // More than two rows
      if (clickedRowIndex === 0) {
        // First row
        moveDownButton.classList.remove("disabled");
        moveBottomButton.classList.remove("disabled");
        removeButton.classList.remove("disabled");
      } else if (clickedRowIndex === totalRows - 1) {
        // Last row
        moveUpButton.classList.remove("disabled");
        moveTopButton.classList.remove("disabled");
        removeButton.classList.remove("disabled");
      } else {
        // Middle rows
        moveUpButton.classList.remove("disabled");
        moveTopButton.classList.remove("disabled");
        moveDownButton.classList.remove("disabled");
        moveBottomButton.classList.remove("disabled");
        removeButton.classList.remove("disabled");
      }
    }
  }
  updateSQLTable() {
    const tableName = document.getElementById("table-name").value;
    document.getElementById("tableName").textContent = tableName;
  }

  updateSQLQuery() {
    const fieldList = document.getElementById("fieldList");
    fieldList.innerHTML = ""; // Clear previous fields

    const rows = document.querySelectorAll(".queryDiv .row");
    rows.forEach((row, index) => {
      if (index === 0) return;
      const fieldName = row.querySelector("input[type='text']").value;
      const fieldType = row.querySelector(".field-type").value;
      let fieldTypeText = "";
      switch (fieldType) {
        case "0":
          fieldTypeText = "INTEGER";
          break;
        case "1":
          fieldTypeText = "TEXT";
          break;
        case "2":
          fieldTypeText = "BLOB";
          break;
        case "3":
          fieldTypeText = "REAL";
          break;
        case "4":
          fieldTypeText = "NUMERIC";
          break;
        default:
          fieldTypeText = "INTEGER";
          break;
      }

      const nullable = row.querySelector(".field-nullable input").checked
        ? "NOT NULL"
        : "";
      const primaryKey = row.querySelector(".field-primary-key input").checked
        ? "PRIMARY KEY"
        : "";
      const autoIncrement = row.querySelector(".field-auto-increment input")
        .checked
        ? "AUTOINCREMENT"
        : "";
      const unique = row.querySelector(".field-unique input").checked
        ? "UNIQUE"
        : "";

      // Field info satırı
      const newFieldElement = document.createElement("div");
      newFieldElement.classList.add("field-c");
      const fieldInfo = `"${fieldName}" ${fieldTypeText} ${nullable} ${unique}`;
      newFieldElement.innerHTML = fieldInfo;
      fieldList.appendChild(newFieldElement);

      // PRIMARY KEY ve AUTOINCREMENT satırı
      if (primaryKey || autoIncrement) {
        const primaryKeyAutoIncElement = document.createElement("div");
        const primaryKeyAutoIncSQL = autoIncrement
          ? `PRIMARY KEY("${fieldName}" AUTOINCREMENT)`
          : `PRIMARY KEY("${fieldName}")`;
        primaryKeyAutoIncElement.innerHTML = primaryKeyAutoIncSQL;
        fieldList.appendChild(primaryKeyAutoIncElement);
      }
    });
  }
  setupCheckboxListeners() {
    const checkboxes = document.querySelectorAll(
      ".queryDiv .row input[type='checkbox']"
    );
    checkboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", (event) => {
        const rowIndex = event.target.closest(".row").dataset.index; // Satırın index değerini al
        if (event) {
          console.log(`Row ${rowIndex} checkbox is checked`);
        } else {
          console.log(`Row ${rowIndex} checkbox is unchecked`);
        }
        updateSQLQuery(rowIndex); // Checkbox durumu değiştiğinde sorguyu güncelle, satırın indexini parametre olarak gönder
      });
    });
  }

  removeSelectedRow() {
    if (this.selectedRow !== null) {
      this.selectedRow.remove();
      this.selectedRow = null;
      this.updateButtonStates();
      this.updateSQLQuery();
      // Son eleman kaldırıldıysa ve başka eleman kalmadıysa margin-top özelliğini tekrar ekle
      const elementCount = document.querySelectorAll(".field-c").length;
      if (elementCount === 0) {
        document.querySelector(".sql-fields").style.marginTop = "20px";
        this.updateButtonStates();
      }
    }
    this.removeLastAddedRow();
    this.updateOkButtonState();
  }

  updateOkButtonState() {
    const rows = document.querySelectorAll(".queryDiv .js-row");
    const okButton = document.querySelector(
      ".modal-footer .btn[type='submit']"
    );

    if (rows.length > 0) {
      okButton.classList.remove("disabled");
    } else {
      okButton.classList.add("disabled");
    }
  }
  updateSQLColumnNumbers() {
    const sqlField = document.querySelector(".sql-field");
    const sqlCol = sqlField.querySelector(".sql-col");

    const existingPs = sqlCol.querySelectorAll(".sql-p");

    // Son numarayı bul
    const lastNumber = parseInt(existingPs[existingPs.length - 1].textContent);

    // Yeni numarayı ekleyerek sonraki numarayı bul
    const nextNumber = lastNumber + 1;

    const p = document.createElement("p");
    p.classList.add("sql-p");
    p.textContent = nextNumber.toString();
    sqlCol.appendChild(p);
  }

  removeLastAddedRow() {
    const sqlField = document.querySelector(".sql-field");
    const sqlCol = sqlField.querySelector(".sql-col");
    const lastP = sqlCol.querySelector(".sql-p:last-child");

    // İlk 3 sabit elemanı korumak için kontrol ekleyin
    if (lastP && parseInt(lastP.textContent) > 3) {
      lastP.remove();
      this.fieldCounter--;
    }
  }

  saveSQL() {
    const fieldList = document.getElementById("fieldList");
    const tableName = document.getElementById("tableName").innerText;

    // Collect SQL fields
    const fields = Array.from(fieldList.querySelectorAll(".field-c"))
      .map((field) => field.innerText)
      .join(", ");

    const sqlQuery = `CREATE TABLE "${tableName}" (${fields});`;

    fetch("/save-sql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ sql: sqlQuery }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.message) {
          alert(data.message);
        } else if (data.error) {
          alert(data.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  async sqlQuerySave() {
    // Önce updateSQLQuery fonksiyonunu çağırarak fieldList'i güncelleyelim
    this.updateSQLQuery();

    const fieldList = document.getElementById("fieldList");
    const fields = fieldList.querySelectorAll(".field-c");
    const tableNameInput = document.getElementById("tableName");
    const tableName = tableNameInput.innerText;
    let sqlQuery = `CREATE TABLE "${tableName}" (`;
    fields.forEach((field, index) => {
      sqlQuery += field.textContent.trim();
      if (index < fields.length - 1) {
        sqlQuery += ", ";
      }
    });
    sqlQuery += ");";

    try {
      const response = await fetch("/create_table", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ sql_query: sqlQuery }),
      });

      const result = await response.json();
      if (response.ok) {
        console.log("Data:", result.message);
      } else {
        alert(result.error || result.message);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  }
}

// Kullanım
const queryDivManager = new QueryDivManager();

queryDivManager.setupCheckboxListeners();

function toggleSqlQuery() {
  var sqlQueryDiv = document.getElementById("sqlQuery");
  var button = document.querySelector(".sql-col button");

  if (sqlQueryDiv.style.display === "none") {
    sqlQueryDiv.style.display = "block";
    button.textContent = "-";
  } else {
    sqlQueryDiv.style.display = "none";
    button.textContent = "+"; // veya herhangi bir metin
  }
}

const closeDatabaseHandler = async () => {
  try {
    const response = await fetch("/close_database", {
      method: "POST",
    });
    if (response.ok) {
      const data = await response.json();
      alert(data.message); // Backend tarafından gönderilen mesajı göster
      dbOpened = false;
      closeFileDB.classList.add("disabled");
      closeDB.classList.add("disabled");
      fad.classList.add("disabled");
      fcd.classList.add("disabled");
      fsp.classList.add("disabled");
      fspa.classList.add("disabled");
      fsa.classList.add("disabled");
      saveProject.classList.add("disabled");
      adDatabase.classList.add("disabled");
      createTable.classList.add("disabled");
      modifyTable.classList.add("disabled");
      deleteTable.classList.add("disabled");
      tableToCSV.classList.add("disabled");
      tableToJSON.classList.add("disabled");
      const la = document.getElementById("large-area");
      la.innerHTML = "";
    } else {
      const data = await response.json();
      console.error("Failed to close the database:", data.error);
    }
  } catch (error) {
    console.error("An error occurred while closing the database:", error);
  }
};

closeFileDB.addEventListener("click", closeDatabaseHandler);
closeDB.addEventListener("click", closeDatabaseHandler);

const openDatabaseHandler = () => {
  fileInput.click();
};

const fileInputChangeHandler = async (event) => {
  const file = event.target.files[0];
  if (file) {
    const fileName = file.name;
    try {
      const response = await fetch("/open_database", {
        method: "POST",
        body: JSON.stringify({ file_name: fileName }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (response.ok) {
        const data = await response.json();
        alert(data.message);

        console.log("Data:", data.table_columns);
        dbOpened = true;
        fad.classList.remove("disabled");
        fcd.classList.remove("disabled");
        fsp.classList.remove("disabled");
        fspa.classList.remove("disabled");
        fsa.classList.remove("disabled");
        saveProject.disabled = false;
        adDatabase.disabled = false;
        closeDB.disabled = false;
        saveProject.classList.remove("disabled");
        adDatabase.classList.remove("disabled");
        closeDB.classList.remove("disabled");
        createTable.classList.remove("disabled");
        modifyTable.classList.remove("disabled");
        deleteTable.classList.remove("disabled");
        compactDB.classList.remove("disabled");
        loadE.classList.remove("disabled");
        integrityCheck.classList.remove("disabled");
        quickIntegrityCheck.classList.remove("disabled");
        fkCheck.classList.remove("disabled");
        optimize.classList.remove("disabled");
        mCT.disabled = false;
        mCI.disabled = false;
        tableToCSV.classList.remove("disabled");
        tableToJSON.classList.remove("disabled");
        console.log("Data:", data.tables);
        csv.classList.remove("disabled");
        mainWindow(data);
      } else {
        const data = await response.json();
        console.error("Failed to open the database:", data.error);
      }
    } catch (error) {
      console.error("An error occurred while opening the database:", error);
    }
  }
};

openDataB.addEventListener("click", openDatabaseHandler);
openDatabase.addEventListener("click", openDatabaseHandler);
fileInput.addEventListener("change", fileInputChangeHandler);

let dbOpened = false;

const openModal = () => {
  modalButton.click();
};

mCT.addEventListener("click", openModal);
createTable.addEventListener("click", openModal);

// cancelButton.addEventListener("click", () => {
//   csv.classList.remove("disabled");
//   clearModal();
// });

csv.addEventListener("click", () => {
  csvFile.click();
});

const csvChangeHandler = async (event) => {
  const csvFile = event.target.files[0];
  if (csvFile) {
    const csvFileName = csvFile.name;
    try {
      const response = await fetch("/open_csv", {
        method: "POST",
        body: JSON.stringify({ csvFile: csvFileName }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const csvImport = document.getElementById("csvImport");
      csvImport.click();
      if (response.ok) {
        const data = await response.json();
        console.log("Data:", data.tables);
        updateCsvPreview(csvFileName);
      } else {
        const data = await response.json();
        console.error("Failed to open the csv:", data.error);
      }
    } catch (error) {
      console.error("An error occurred while opening the csv:", error);
    }
  }
};

csvFile.addEventListener("change", csvChangeHandler);

const updateCsvPreview = async (csvFileName) => {
  const columnNamesCheckbox = document.getElementById("colNameCheckBox");
  const fieldSeparatorSelect = document.getElementById("fieldSeparator");
  const quoteCharacterSelect = document.getElementById("quoteCharacter");
  const encodingSelect = document.getElementById("encoding");
  const trimFieldsCheckbox = document.getElementById("trimFields");

  if (
    !columnNamesCheckbox ||
    !fieldSeparatorSelect ||
    !quoteCharacterSelect ||
    !encodingSelect ||
    !trimFieldsCheckbox
  ) {
    console.error("One or more elements not found");
    return;
  }

  const settings = {
    columnNamesInFirstLine: columnNamesCheckbox.checked,
    fieldSeparator: fieldSeparatorSelect.value,
    quoteCharacter: quoteCharacterSelect.value || '"',
    encoding: encodingSelect.value,
    trimFields: trimFieldsCheckbox.checked,
  };

  try {
    const response = await fetch("/update_csv_preview", {
      method: "POST",
      body: JSON.stringify({ csvFile: csvFileName, settings: settings }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      const data = await response.json();
      const previewElement = document.getElementById("csvPreview"); // Update to your actual preview element ID
      if (!previewElement) {
        console.error("Preview element not found");
        return;
      }
      handleCsvPreviewResponse(data);
      previewElement.innerHTML = generateTableHTML(
        data.tables,
        data.column_names
      );
    } else {
      const data = await response.json();
      console.error("Failed to update the preview:", data.error);
    }
  } catch (error) {
    console.error("An error occurred while updating the preview:", error);
  }
};

const generateTableHTML = (rows, columns) => {
  let tableHTML = '<table class="table"><thead><tr>';
  columns.forEach((column, index) => {
    tableHTML += `<th>field${index + 1}</th>`;
  });
  tableHTML += "</tr></thead><tbody>";
  rows.forEach((row) => {
    tableHTML += "<tr>";
    row.forEach((cell) => {
      tableHTML += `<td>${cell}</td>`;
    });
    tableHTML += "</tr>";
  });
  tableHTML += "</tbody></table>";
  return tableHTML;
};

const columnNamesCheckbox = document.getElementById("colNameCheckBox");

columnNamesCheckbox.addEventListener("change", function () {
  const checked = this.checked;
  const previewElement = document.getElementById("csvPreview");
  const thElements = previewElement.querySelectorAll("thead th");
  const tbodyElement = previewElement.querySelector("tbody");

  // Güncelleme işlemi
  if (checked) {
    thElements.forEach((th, index) => {
      th.textContent = colNames[index];
    });
    // İlk satırı tbody'dan kaldırıyoruz
    const firstRow = tbodyElement.querySelector("tr");
    if (firstRow) {
      tbodyElement.removeChild(firstRow);
    }
  } else {
    thElements.forEach((th, index) => {
      th.textContent = `field${index + 1}`;
    });
    // İlk satırı geri ekliyoruz
    const newRow = document.createElement("tr");
    colNames.forEach((name, index) => {
      const newCell = document.createElement("td");
      newCell.textContent = colNames[index];
      newRow.appendChild(newCell);
    });
    tbodyElement.insertBefore(newRow, tbodyElement.firstChild);
  }
});
let colNames = [];
const handleCsvPreviewResponse = (data) => {
  colNames = data.tables[0];
};

class csvManager {
  constructor() {
    this.csvOKButton = document.getElementById("csvOK");
    this.csvTableNameInput = document.getElementById("csvTableName");
    this.isListenerAdded = false;

    this.setupCsvInputListener();
    this.addCsvButtonClickListener();
  }

  setupCsvInputListener() {
    this.csvTableNameInput.addEventListener("keyup", () => {
      const tableName = this.csvTableNameInput.value.trim();
      if (tableName) {
        this.csvOKButton.classList.remove("disabled");
      } else {
        this.csvOKButton.classList.add("disabled");
      }
    });
  }

  addCsvButtonClickListener() {
    if (this.isListenerAdded) return;

    this.csvOKButton.addEventListener("click", async () => {
      const tableName = this.csvTableNameInput.value.trim();
      if (!tableName) return;

      try {
        const response = await fetch("/add_csv_to_db", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            table_name: tableName,
            // CSV ve DB dosya yolları gerekli parametrelerle eklenmeli
            csv_file_path: "path/to/your/csvfile.csv",
            db_file_path: "path/to/your/database.db",
          }),
        });

        if (response.ok) {
          const data = await response.json();
          console.log("Success:", data.message);
          const csvCancel = document.getElementById("csvCancel");
          csvCancel.click();
        } else {
          const errorData = await response.json();
          console.error("Error:", errorData.error);
        }
      } catch (error) {
        console.error("An error occurred:", error);
      }
    });

    this.isListenerAdded = true;
  }
}

const csvM = new csvManager();
csvM.addCsvButtonClickListener();

let isRotated = false;
const mainWindow = (data) => {
  const len = data.tables.length;
  const collapseCol = document.getElementById("collapseCol");
  const rowcover = document.createElement("div");
  const collapseType = document.getElementById("collapseType");
  rowcover.classList.add("row");
  const row = document.getElementById("collapseTables");

  const p = document.createElement("p");
  const pClass = ["d-inline-flex", "gap-1"];
  pClass.forEach((cls) => p.classList.add(cls));

  const button = document.createElement("button");
  button.classList.add("btn");
  button.type = "button";
  button.setAttribute("data-bs-toggle", "collapse");
  button.setAttribute("data-bs-target", "#Tables");
  button.ariaExpanded = "false";
  button.ariaControls = "Tables";
  button.style.bottom = "-10px";
  button.style.position = "relative";
  const img1 = document.createElement("img");
  const img2 = document.createElement("img");
  img1.src = "/static/icons/bullet_arrow_up.svg";
  img1.style.transform = "rotate(90deg)";
  img1.style.left = "-15px";
  img1.style.position = "relative";
  img1.style.top = "-2px";
  img1.id = "rotateImg";
  img2.src = "/static/icons/table.svg";
  img2.style.position = "relative";
  img2.style.top = "-2px";
  img2.style.left = "-3px";
  img2.style.width = "20px";
  button.appendChild(img1);
  button.appendChild(img2);
  button.appendChild(document.createTextNode(`Tables (${len})`));
  p.appendChild(button);
  row.appendChild(p);

  data.tables.forEach((tableName, index) => {
    const tablediv = document.createElement("div");
    tablediv.classList.add("collapse");
    tablediv.id = "Tables";
    const innerbutton = document.createElement("button");
    innerbutton.classList.add("btn");
    innerbutton.type = "button";
    innerbutton.setAttribute("data-bs-toggle", "collapse");
    innerbutton.setAttribute("data-bs-target", `#Tables${index}`);
    innerbutton.ariaExpanded = "false";
    innerbutton.ariaControls = `Tables${index}`;
    innerbutton.style.marginLeft = "30px";
    innerbutton.textContent = tableName;
    tablediv.appendChild(innerbutton);
    row.appendChild(tablediv);

    const columns = data.table_columns[tableName];
    const innerdiv = document.createElement("div");
    innerdiv.classList.add("collapse");
    innerdiv.id = `Tables${index}`;
    columns.forEach((column, columnIndex) => {
      const innerdiv2 = document.createElement("div");
      innerdiv2.classList.add("card", "card-body");
      innerdiv2.style.marginLeft = "100px";
      innerdiv2.textContent = column.name;
      collapseType.textContent = column.type;
      innerdiv.appendChild(innerdiv2);

      // row.appendChild(innerdiv); // tablediv'e eklemeliyiz, row'a değil
    });
    row.appendChild(innerdiv);
  });
  const row1 = document.createElement("div");
  row1.classList.add("row");
  row1.style.marginTop = "-5px";
  row1.style.marginLeft = "12px";
  row1.style.marginBottom = "20px";
  const iconImg = document.createElement("img");
  iconImg.src = "/static/icons/tag_blue.svg";
  iconImg.style.width = "auto";
  iconImg.style.height = "auto";
  iconImg.style.position = "relative";
  const textNode = document.createTextNode("Indices (0)");
  row1.appendChild(iconImg);
  row1.appendChild(textNode);
  collapseCol.appendChild(row1);
  collapseCol.appendChild(row1);
  const row2 = document.createElement("div");
  row2.classList.add("row");
  row2.style.marginTop = "-5px";
  row2.style.marginLeft = "12px";
  row2.style.marginBottom = "20px";
  const iconImg2 = document.createElement("img");
  iconImg2.src = "/static/icons/picture.svg";
  iconImg2.style.width = "auto";
  iconImg2.style.height = "auto";
  iconImg2.style.position = "relative";
  const textNode2 = document.createTextNode("View (0)");
  row2.appendChild(iconImg2);
  row2.appendChild(textNode2);
  collapseCol.appendChild(row2);
  const row3 = document.createElement("div");
  row3.classList.add("row");
  row3.style.marginTop = "-5px";
  row3.style.marginLeft = "12px";
  row3.style.marginBottom = "20px";
  const iconImg3 = document.createElement("img");
  iconImg3.src = "/static/icons/script.svg";
  iconImg3.style.width = "auto";
  iconImg3.style.height = "auto";
  iconImg3.style.position = "relative";
  const textNode3 = document.createTextNode("Trigger (0)");
  row3.appendChild(iconImg3);
  row3.appendChild(textNode3);
  collapseCol.appendChild(row3);

  // Add event listener to rotate the image
  button.addEventListener("click", () => {
    isRotated = !isRotated;
    img1.style.transform = isRotated ? "rotate(180deg)" : "rotate(90deg)";
  });
};

const exportJson = document.getElementById("ejson");
tableToJSON.addEventListener("click", async () => {
  exportJson.click();
});

let selectedTables = [];
document.getElementById("ejson").addEventListener("click", async () => {
  try {
    const response = await fetch("/get_table_names");
    const data = await response.json();
    if (response.ok) {
      const tableNames = data.table_names;
      const tableNamesDiv = document.getElementById("tabletoJson");

      // Önce mevcut tablo adlarını temizleyin
      tableNamesDiv.innerHTML = "";

      // Tablo adlarını div içine ekleyin
      tableNames.forEach((tableName) => {
        const tableNameElement = document.createElement("div");
        tableNameElement.textContent = tableName;
        tableNameElement.classList.add("tableName");

        // Tablo adının tıklama olayını dinleyin
        tableNameElement.addEventListener("click", function () {
          // Seçili hale gelip gelmediğini kontrol edin
          if (this.classList.contains("selected")) {
            // Eğer seçiliyse, seçili sınıfını kaldırın
            this.classList.remove("selected");
            // Ve seçili tablo adını seçilmiş tablolar listesinden kaldırın
            selectedTables = selectedTables.filter(
              (table) => table !== tableName
            );
          } else {
            // Değilse, seçili sınıfını ekleyin
            this.classList.add("selected");
            // Ve seçili tablo adını seçilmiş tablolar listesine ekleyin
            selectedTables.push(tableName);
          }
          // Arka plan rengini değiştirin
          this.style.backgroundColor = this.classList.contains("selected")
            ? "orange"
            : "";
          // // Seçilmiş tablo adlarını konsola yazdırın (opsiyonel)
          // console.log("Selected tables:", selectedTables);
        });

        // Tablo adını div içine ekleyin
        tableNamesDiv.appendChild(tableNameElement);
      });
    } else {
      alert(data.error || data.message);
    }
  } catch (error) {
    console.error("An error occurred while fetching table names:", error);
  }
});

document.getElementById("JSONSave").addEventListener("click", async () => {
  try {
    // Seçili tablo adlarını backend'e göndermek için fetch isteği yapın
    const response = await fetch("/save_json", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ selectedTables: selectedTables }),
    });
    // Sunucudan gelen cevabı kontrol edin
    if (response.ok) {
      const data = await response.json();
      console.log("Selected tables successfully converted to JSON", data);
      const JSONCancel = document.getElementById("JSONCancel");
      JSONCancel.click();
    } else {
      // İşlem başarısızsa, hata mesajını gösterin
      const errorData = await response.json();
      console.error("Error:", errorData.error || errorData.message);
    }
  } catch (error) {
    // Hata durumunda konsola yazdırın
    console.error("An error occurred while sending selected tables:", error);
  }
});

tableToCSV.addEventListener("click", async () => {
  const csvBut = document.getElementById("csvBut");
  csvBut.click();
});

let csvSelectedTables = [];
document.getElementById("csvBut").addEventListener("click", async () => {
  try {
    const response = await fetch("/get_table_names");
    const data = await response.json();
    if (response.ok) {
      const tableNames = data.table_names;
      const tableNamesDiv = document.getElementById("tabletoCSV");

      // Önce mevcut tablo adlarını temizleyin
      tableNamesDiv.innerHTML = "";

      // Tablo adlarını div içine ekleyin
      tableNames.forEach((tableName) => {
        const tableNameElement = document.createElement("div");
        tableNameElement.textContent = tableName;
        tableNameElement.classList.add("tableName");

        // Tablo adının tıklama olayını dinleyin
        tableNameElement.addEventListener("click", function () {
          // Seçili hale gelip gelmediğini kontrol edin
          if (this.classList.contains("selected")) {
            // Eğer seçiliyse, seçili sınıfını kaldırın
            this.classList.remove("selected");
            // Ve seçili tablo adını seçilmiş tablolar listesinden kaldırın
            csvSelectedTables = csvSelectedTables.filter(
              (table) => table !== tableName
            );
          } else {
            // Değilse, seçili sınıfını ekleyin
            this.classList.add("selected");
            // Ve seçili tablo adını seçilmiş tablolar listesine ekleyin
            csvSelectedTables.push(tableName);
          }
          // Arka plan rengini değiştirin
          this.style.backgroundColor = this.classList.contains("selected")
            ? "orange"
            : "";
          // // Seçilmiş tablo adlarını konsola yazdırın (opsiyonel)
          // console.log("Selected tables:", selectedTables);
        });

        // Tablo adını div içine ekleyin
        tableNamesDiv.appendChild(tableNameElement);
      });
    } else {
      alert(data.error || data.message);
    }
  } catch (error) {
    console.error("An error occurred while fetching table names:", error);
  }
});

document.getElementById("CSVSave").addEventListener("click", async () => {
  try {
    // Seçilen tablo adlarını içeren dizi
    const selectedTables = csvSelectedTables;

    // Seçili tablo adlarını backend'e gönder
    const response = await fetch("/save_csv", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ selectedTables: selectedTables }),
    });
    // Yanıtı kontrol et ve mesajı göster
    const data = await response.json();
    if (response.ok) {
      console.log(data.message);
      const CSVCancel = document.getElementById("CSVCancel");
      CSVCancel.click();
    } else {
      alert(data.error || data.message);
    }
  } catch (error) {
    console.error("An error occurred while saving JSON:", error);
  }
});
