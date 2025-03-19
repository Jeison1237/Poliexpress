document.addEventListener("DOMContentLoaded", function() {
    console.log("Poliexpress está listo!");

    document.getElementById("buscador").addEventListener("keyup", function() {
        let filtro = this.value.toLowerCase();
        let productos = document.querySelectorAll(".producto");
        productos.forEach(prod => {
            let nombre = prod.querySelector("h3").textContent.toLowerCase();
            prod.style.display = nombre.includes(filtro) ? "block" : "none";
        });
    });
});

function agregarAlCarrito(productoId) {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    carrito.push(productoId);
    localStorage.setItem("carrito", JSON.stringify(carrito));
    alert("Producto agregado al carrito!");
}