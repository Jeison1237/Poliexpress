document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Poliexpress está listo!");

    // === Buscador de productos ===
    const buscador = document.getElementById("buscador");
    if (buscador) {
        buscador.addEventListener("keyup", function () {
            const filtro = this.value.toLowerCase();
            document.querySelectorAll(".producto").forEach(prod => {
                const nombre = prod.querySelector("h3")?.textContent.toLowerCase() || "";
                prod.style.display = nombre.includes(filtro) ? "block" : "none";
            });
        });
    }

    // === Navbar con efecto scroll ===
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        window.addEventListener("scroll", () => {
            navbar.classList.toggle("navbar-scroll", window.scrollY > 50);
        });
    }

    // === Modo Oscuro con LocalStorage ===
    const toggleDark = document.getElementById("toggle-dark");
    const aplicarModoOscuro = (activar) => {
        document.body.classList.toggle("dark-mode", activar);
        navbar?.classList.toggle("navbar-dark-mode", activar);
        localStorage.setItem("darkMode", activar);
    };

    if (toggleDark) {
        const darkModeActivo = localStorage.getItem("darkMode") === "true";
        aplicarModoOscuro(darkModeActivo);

        toggleDark.addEventListener("click", () => {
            const activado = !document.body.classList.contains("dark-mode");
            aplicarModoOscuro(activado);
        });
    }

    // === Carrito de Compras (modo local) ===
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const contenedorCarrito = document.getElementById("carrito");
    const contadorCarrito = document.getElementById("contador-carrito");

    function actualizarCarritoUI() {
        if (contenedorCarrito && contadorCarrito) {
            contenedorCarrito.innerHTML = "";
            let totalItems = 0;

            carrito.forEach(item => {
                const li = document.createElement("li");
                li.classList.add("list-group-item");
                li.textContent = `${item.nombre} - ${item.cantidad}`;
                contenedorCarrito.appendChild(li);
                totalItems += item.cantidad;
            });

            contadorCarrito.textContent = totalItems;
        }
    }

    // === Botones "Ordenar" para agregar al carrito (función con redirección) ===
    document.querySelectorAll(".ordenar-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            const id = this.getAttribute("data-id");
            if (id) {
                window.location.href = `/pedidos/agregar_al_carrito/${id}/`;
            }
        });
    });

    // === Validación en formularios (login y registro) ===
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function (e) {
            let valid = true;

            form.querySelectorAll("input").forEach(input => {
                const vacio = input.value.trim() === "";
                input.style.borderColor = vacio ? "#dc3545" : "#ccc";
                if (vacio) valid = false;
            });

            if (!valid) {
                e.preventDefault();
                alert("Completa todos los campos antes de continuar.");
            }
        });
    });

    // === Autofocus al primer input de formularios ===
    const firstInput = document.querySelector("form input");
    if (firstInput) {
        firstInput.focus();
    }

    // === Inicializar UI si el carrito existe ===
    actualizarCarritoUI();
});
