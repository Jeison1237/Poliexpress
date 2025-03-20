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

    window.agregarAlCarrito = function (id, nombre, precio) {
        let producto = carrito.find(item => item.id === id);
        if (producto) {
            producto.cantidad++;
        } else {
            carrito.push({ id, nombre, precio, cantidad: 1 });
        }
        localStorage.setItem("carrito", JSON.stringify(carrito));
        actualizarCarritoUI();
    };

    actualizarCarritoUI();
});
