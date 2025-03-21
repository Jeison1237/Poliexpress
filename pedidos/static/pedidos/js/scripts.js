document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Poliexpress está listo!");

    /* ====== Buscador de productos ====== */
    let buscador = document.getElementById("buscador");
    if (buscador) {
        buscador.addEventListener("keyup", function () {
            let filtro = this.value.toLowerCase();
            document.querySelectorAll(".producto").forEach(prod => {
                let nombre = prod.querySelector("h3").textContent.toLowerCase();
                prod.style.display = nombre.includes(filtro) ? "block" : "none";
            });
        });
    }

    /* ====== Navbar: efecto al hacer scroll ====== */
    let navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", function () {
            navbar.classList.toggle("navbar-scroll", window.scrollY > 50);
        });
    }

    /* ====== Modo Oscuro con LocalStorage ====== */
    const toggleDark = document.getElementById("toggle-dark");
    if (toggleDark) {
        if (localStorage.getItem("darkMode") === "true") {
            document.body.classList.add("dark-mode");
            navbar?.classList.add("navbar-dark-mode");
        }

        toggleDark.addEventListener("click", function () {
            let isDark = document.body.classList.toggle("dark-mode");
            navbar?.classList.toggle("navbar-dark-mode", isDark);
            localStorage.setItem("darkMode", isDark);
        });
    }

    /* ====== Carrito de Compras ====== */
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const contenedorCarrito = document.getElementById("carrito");
    const contadorCarrito = document.getElementById("contador-carrito");

    function actualizarCarritoUI() {
        if (contenedorCarrito && contadorCarrito) {
            contenedorCarrito.innerHTML = "";
            let totalItems = 0;
            carrito.forEach(item => {
                let li = document.createElement("li");
                li.classList.add("list-group-item");
                li.textContent = `${item.nombre} - ${item.cantidad}`;
                contenedorCarrito.appendChild(li);
                totalItems += item.cantidad;
            });
            contadorCarrito.textContent = totalItems;
        }
    }

    function agregarAlCarrito(id) {
        fetch("/agregar_al_carrito/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCookie("csrftoken") // Necesario en Django para seguridad
            },
            body: `producto_id=${id}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Producto agregado al carrito");
            } else {
                alert("Error al agregar al carrito");
            }
        })
        .catch(error => console.error("Error:", error));
    }
    
    // Función para obtener CSRF token (Django lo usa para seguridad en POST requests)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            let cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
});
