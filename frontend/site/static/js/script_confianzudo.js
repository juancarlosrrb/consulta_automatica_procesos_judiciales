//comunicación front y backend

//1. Registro
const base_url = window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:5000'  // Puerto local
    : 'https://consulta-automatica-procesos-judiciales.onrender.com';  // URL de producción


// Función para mostrar/ocultar la contraseña principal
function togglePasswordVisibility(passwordFieldId, checkboxId) {
    const passwordField = document.getElementById(passwordFieldId);
    const checkbox = document.getElementById(checkboxId);

    checkbox.addEventListener('change', function () {
        passwordField.type = this.checked ? 'text' : 'password';
    });
}

// Inicializa la funcionalidad de mostrar/ocultar contraseñas
function initializePasswordToggle() {
    togglePasswordVisibility('password_registro', 'mostrar_password');
    togglePasswordVisibility('password_confirmacion_registro', 'mostrar_confirmacion_password');
}

// Llama a la inicialización cuando la página esté lista
document.addEventListener('DOMContentLoaded', initializePasswordToggle);

// Asignar el evento al formulario cuando la página se cargue
document.getElementById('registro-form').addEventListener('submit', manejarFormulario);

// Función para mostrar el mensaje en el HTML
function mostrarMensaje(mensaje) {
    document.getElementById('mensaje').innerText = mensaje;
}

// Función para validar contraseña
function validarPassword(password) {
    const longitudMinima = 8;
    const tieneMayuscula = /[A-Z]/.test(password); // Al menos una letra mayúscula
    const tieneMinuscula = /[a-z]/.test(password); // Al menos una letra minúscula
    const tieneNumero = /[0-9]/.test(password); // Al menos un número
    const tieneEspecial = /[@#$%^&*(),.?":{}|<>]/.test(password); // Al menos un carácter especial

    if (
        password.length < longitudMinima ||
        !tieneMayuscula ||
        !tieneMinuscula ||
        !tieneNumero ||
        !tieneEspecial
    ) {
        return false; // No cumple con los requisitos
    }
    return true; // Cumple con los requisitos
}


// Función que maneja el evento submit del formulario
function manejarFormulario(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado del formulario

    const correo = document.getElementById('username_registro').value;
    const password = document.getElementById('password_registro').value;
    const password_confirmacion = document.getElementById('password_confirmacion_registro').value;

    // Validar que las contraseñas coincidan
    if (password !== password_confirmacion) {
        mostrarMensaje('Error: Las contraseñas no coinciden.');
        return;
    }

    // Validar que la contraseña sea compleja
    if (!validarPassword(password)) {
        mostrarMensaje('Error: La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales.');
        return;
    }

    // Validar el formato del correo
    const correoRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Expresión regular para correos válidos
    if (!correoRegex.test(correo)) {
        mostrarMensaje('Error: Introduzca un correo válido.');
        return;
    }


    mostrarMensaje('Validaciones superadas, enviando datos...');

    // Llamada a la función que envía el formulario y maneja la respuesta
    enviar_registrar_usuario(correo, password)
        .then(data => {
            if (data) {
                mostrarMensaje(`Respuesta: ${data.mensaje}`);
            } else {
                mostrarMensaje('Error al conectar con el servidor');
            }
        })
        .catch(error => {
            console.error('Error al enviar los datos:', error);
            mostrarMensaje('Ocurrió un error inesperado.');
        });
}

// Función que maneja el envío del formulario
async function enviar_registrar_usuario(correo, password) {
    const codigo_ingresado_dom = document.getElementById('token_input'); // Obtenemos el elemento DOM
    codigo_ingresado_dom.value = ""; //Resetea el valor del código ingresado después de enviar


    try {
        const respuesta = await fetch(`${base_url}/correo_registrar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mail_username: correo, password_sfa: password })
        });

        const data = await respuesta.json();

        if (data.mensaje === "Correo enviado con el código de verificación. Por favor, ingresa el código de 4 dígitos enviado a tu correo.") {
            // Mostrar el campo para ingresar el token
            mostrarCampoToken();

        }

        return data; // Retorna la respuesta para manejarla más tarde
    } catch (error) {
        console.error('Error:', error);
        return null; // Retorna null en caso de error
    }
}

// Función que agrega el campo para ingresar el token debajo de "Confirmar Contraseña"
function mostrarCampoToken() {
    // Mostrar el campo para ingresar el token
    document.getElementById("token-div").style.display = "block"    
}


// Función que maneja el envío del formulario
async function verificar_codigo(correo) {

    event.preventDefault();  // Evita el comportamiento predeterminado del formulario

    const correo_token = document.getElementById('username_registro').value;
    const password_token = document.getElementById('password_registro').value;
    const codigo_ingresado = document.getElementById('token_input').value;
    const codigo_ingresado_dom = document.getElementById('token_input'); // Obtenemos el elemento DOM
    

    try {
        const respuesta = await fetch('http://127.0.0.1:5000/verificar_codigo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mail_username: correo_token, password_sfa: password_token, codigo_ingresado: codigo_ingresado })
        });

        const data = await respuesta.json();
        document.getElementById('mensaje_exitoso').innerText = "";
        document.getElementById('mensaje_exitoso').innerText = data.mensaje;

        return data; // Retorna la respuesta para manejarla más tarde

    } catch (error) {
        console.error('Error:', error);
        return null; // Retorna null en caso de error
    } finally {
        // Limpiar el campo de entrada de archivo
        codigo_ingresado_dom.value = ""; //Resetea el valor del código ingresado después de enviar
    }
}


// Asignar el evento al formulario cuando la página se cargue
document.getElementById('login-form').addEventListener('submit', correo_login);

//Función para loggear al usuario
async function correo_login(event1) {
    event1.preventDefault(); // Evita el comportamiento predeterminado del botón

    
    const correo = document.getElementById("correo_login").value;
    const password = document.getElementById("password_login").value;


    try {
        const respuesta = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mail_username: correo, password_sfa: password })
        });

        const data = await respuesta.json();

        if (data.success) {
            // Almacenar el correo en sessionStorage para identificar al usuario
            sessionStorage.setItem("correo", correo);

            console.log(data)
            console.log(correo)
            // Redirigir al dashboard
            window.location.href = "seguimiento_procesos_judiciales.html";
        } else {
            alert(data.mensaje); // Mostrar mensaje de error
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error al iniciar sesión. Inténtalo nuevamente.");
    }
}
