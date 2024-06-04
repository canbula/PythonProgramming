// Sidebar genişliğini ayarlama
var sidebar = document.getElementById("sidebar");  // Sidebar elemanını al
var currentWidth = sidebar.offsetWidth;  // Mevcut genişliği al
var newWidth = currentWidth / 2;  // Yarıya kadar küçült
sidebar.style.width = newWidth + "px";  // Yeni genişliği uygula
