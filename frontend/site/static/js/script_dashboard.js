//verificar que se ha iniciado sesión y si no reenviar a home page
document.addEventListener("DOMContentLoaded", function () {
    verificacion_logeo(); // Llama la función automáticamente al cargar la página
    mostrar_procesos_judiciales_del_cliente(); //carga los procesos judiciales del cliente
});

function verificacion_logeo() {

		const correo = localStorage.getItem("correo"); // O sessionStorage

	    console.log(correo);
	    document.getElementById('usuario-correo').innerText = correo;

	    if (!correo) {
	        // Si no hay un correo almacenado, redirigir a la página de login
	        alert("Por favor, inicia sesión primero.");
	        window.location.href = "login.html";
            //<a href="{{ url_for('login') }}">

	    } 
}


function cerrarSesion() {
    // Limpia el sessionStorage y redirige al login
    sessionStorage.clear();
    window.location.href = "login.html";
}

// Función para agregar un proceso
async function agregar_numero_radicado() {
	const correo = sessionStorage.getItem("correo");
    const numeroDeRadicado = document.getElementById("numero_radicado").value;
    const mensaje = document.getElementById("mensaje_agregar");

    // Validación básica de campos
    if (!correo || !numeroDeRadicado) {
        mensaje.innerText = "Por favor, completa todos los campos.";
        mensaje.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/agregar_proceso", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ correo: correo, numero_de_radicado: numeroDeRadicado }),
        });

        const data = await response.json();

        if (data.success) {
            mensaje.innerText = data.message;
            mensaje.style.color = "green";
        } else {
            mensaje.innerText = data.message;
            mensaje.style.color = "red";
        }
    } catch (error) {
        mensaje.innerText = "Hubo un error al procesar la solicitud.";
        mensaje.style.color = "red";
        //console.error("Error:", error);
    }
}

// Función para agregar un proceso
async function agregar_numero_radicado() {
	const correo = sessionStorage.getItem("correo");
    const numeroDeRadicado = document.getElementById("numero_radicado").value;
    const mensaje = document.getElementById("mensaje_agregar");

    // Validación básica de campos
    if (!correo || !numeroDeRadicado) {
        mensaje.innerText = "Por favor, completa todos los campos.";
        mensaje.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/agregar_proceso", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ correo: correo, numero_de_radicado: numeroDeRadicado }),
        });

        const data = await response.json();

        if (data.success) {
            mensaje.innerText = data.message;
            mensaje.style.color = "green";
            mostrar_procesos_judiciales_del_cliente()
        } else {
            mensaje.innerText = data.message;
            mensaje.style.color = "red";
        }
    } catch (error) {
        mensaje.innerText = "Hubo un error al procesar la solicitud.";
        mensaje.style.color = "red";
        //console.error("Error:", error);
    }
}

// Función para eliminar un proceso
async function eliminar_numero_radicado() {
	const correo = sessionStorage.getItem("correo");
    const numeroDeRadicado = document.getElementById("numero_radicado").value;
    const mensaje = document.getElementById("mensaje_agregar");

    // Validación básica de campos
    if (!correo || !numeroDeRadicado) {
        mensaje.innerText = "Por favor, completa todos los campos.";
        mensaje.style.color = "red";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/eliminar_proceso", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ correo: correo, numero_de_radicado: numeroDeRadicado }),
        });

        const data = await response.json();

        if (data.success) {
            mensaje.innerText = data.message;
            mensaje.style.color = "green";
            mostrar_procesos_judiciales_del_cliente()

        } else {
            mensaje.innerText = data.message;
            mensaje.style.color = "red";
        }
    } catch (error) {
        mensaje.innerText = "Hubo un error al procesar la solicitud.";
        mensaje.style.color = "red";
        //console.error("Error:", error);
    }
}


async function buscar_n_radicado() {

	const correo = sessionStorage.getItem("correo");
    const numeroDeRadicado = document.getElementById("numero_radicado").value;
    const mensaje = document.getElementById("mensaje_agregar");

    try {
        const response = await fetch('http://127.0.0.1:5000/buscar_proceso', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                correo: correo,
                numero_de_radicado: numeroDeRadicado
            })
        });

        const data = await response.json();

        if (data.success) {
            mensaje.innerText = data.message;
            mensaje.style.color = "green";
        } else {
            mensaje.innerText = data.message;
            mensaje.style.color = "red";
        }

        if (result.success) {
            messageElement.style.color = 'green'; // Color verde para éxito
        } else {
            messageElement.style.color = 'red'; // Color rojo para error
        }
    } catch (error) {
        //console.error('Error al buscar el proceso:', error);
    }
};

//mostrar procesos judiciales del coreo
async function mostrar_procesos_judiciales_del_cliente() {
    // Obtener el correo desde sessionStorage
    const correo = sessionStorage.getItem('correo');

    try {
        const response = await fetch(`http://127.0.0.1:5000/listar_procesos?correo=${correo}`);
        const result = await response.json();

        if (result.success) {
            const procesos = result.procesos;
            const tabla = document.getElementById('tabla-procesos');
            tabla.innerHTML = '';  // Limpiar tabla

            // Agregar procesos a la tabla
            if (procesos.length > 0) {
                procesos.forEach((radicado) => {
                    const row = document.createElement('tr');
                    const cell = document.createElement('td');
                    cell.textContent = radicado;
                    row.appendChild(cell);
                    tabla.appendChild(row);
                });
            } else {
                const row = document.createElement('tr');
                const cell = document.createElement('td');
                cell.colSpan = 1;
                cell.textContent = 'No hay procesos registrados.';
                row.appendChild(cell);
                tabla.appendChild(row);
            }
        } else {
            alert(result.message);
        }
    } catch (error) {
        //console.error('Error al obtener los procesos:', error);
    }
};


// Función para manejar el clic del botón y descargar el archivo Excel
// Función para manejar el clic del botón y descargar el archivo Excel

async function generar_reporte_excel() {
    const botonDescarga = document.getElementById("descargarBtn");
    const spinner = document.getElementById("spinner");
    const mensajeEstado = document.getElementById("mensaje-estado");

    try {
        // Mostrar el spinner y deshabilitar el botón
        spinner.classList.remove("d-none");
        botonDescarga.disabled = true;
        mensajeEstado.textContent = "Generando el archivo. Por favor, espera...";

        const correo = sessionStorage.getItem("correo");

        const response = await fetch('http://127.0.0.1:5000/generar_reporte', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correo: correo })
        });

        if (!response.ok) {
            throw new Error('Error al generar el archivo Excel.');
        }

        // Procesar el archivo descargado
        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `consulta_procesos_${correo}.xlsx`;       
        link.click();

        // Actualizar el mensaje de estado
        mensajeEstado.textContent = "Archivo descargado exitosamente.";
    } catch (error) {
        mensajeEstado.textContent = "Hubo un error al generar el archivo.";
        console.error(error);
    } finally {
        // Ocultar el spinner y habilitar el botón
        spinner.classList.add("d-none");
        botonDescarga.disabled = false;
    }
}

//Cargar varios procesos
// Cargar varios procesos
async function cargar_varios_procesos() {
    const archivoInput = document.getElementById('archivoRadicados');
    const archivo = archivoInput.files[0];
    const mensajeEstado = document.getElementById("mensaje-estado");

    if (!archivo) {
        mensajeEstado.textContent = "Por favor, selecciona un archivo.";
        return;
    }

    const correo = sessionStorage.getItem("correo"); // Obtener el correo desde sessionStorage

    // Verificar que el correo existe
    if (!correo) {
        mensajeEstado.textContent = "No se encontró el correo asociado.";
        return;
    }

    // Crear un FormData para enviar el archivo y el correo al backend
    const formData = new FormData();
    formData.append("archivo", archivo);
    formData.append("correo", correo); // Añadir el correo al FormData

    try {
        // Mostrar el mensaje de carga
        mensajeEstado.textContent = "Cargando el archivo...";

        const response = await fetch('http://127.0.0.1:5000/cargar_varios_procesos', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Error al cargar los radicados.');
        }

        const data = await response.json();
        mensajeEstado.textContent = data.message; // Mensaje de éxito o error

        // Mostrar procesos judiciales
        mostrar_procesos_judiciales_del_cliente();

    } catch (error) {
        mensajeEstado.textContent = "Hubo un error al cargar el archivo.";
        console.error(error);
    } finally {
        // Limpiar el campo de entrada de archivo
        archivoInput.value = ""; // Resetea el valor del input

    }
}
