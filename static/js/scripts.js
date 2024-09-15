// Manejo del menú móvil
document.addEventListener("DOMContentLoaded", function() {
    const menuIcon = document.getElementById("menu-icon");
    const mobileMenu = document.getElementById("mobile-menu");
  
    menuIcon.addEventListener("click", function() {
        // Alterna la visibilidad del menú móvil
        if (mobileMenu.style.display === "none" || mobileMenu.style.display === "") {
            mobileMenu.style.display = "flex";
        } else {
            mobileMenu.style.display = "none";
        }
    });
  });
  
  // Función para manejar las pestañas (tabs)
  function openTab(evt, tabName) {
      // Oculta todo el contenido de las tabs
      var tabcontent = document.getElementsByClassName("tabcontent");
      for (var i = 0; i < tabcontent.length; i++) {
          tabcontent[i].style.display = "none";
      }
      
      // Remueve la clase "active" de todos los botones de tabs
      var tablinks = document.getElementsByClassName("tablink");
      for (var i = 0; i < tablinks.length; i++) {
          tablinks[i].classList.remove("active");
      }
      
      // Muestra el contenido del tab actual y añade la clase "active" al botón
      document.getElementById(tabName).style.display = "block";
      evt.currentTarget.classList.add("active");
  }
  