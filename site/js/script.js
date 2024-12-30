//comunicación front y backend
// Función que maneja el envío del formulario
async function enviarFormulario(correo, password) {
    try {
        const respuesta = await fetch('http://127.0.0.1:5000/correo_login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mail_username: correo, password_sfa: password })
        });

        const data = await respuesta.json();
        return data; // Retorna la respuesta para manejarla más tarde
    } catch (error) {
        console.error('Error:', error);
        return null; // Retorna null en caso de error
    }
}

// Función para mostrar el mensaje en el HTML
function mostrarMensaje(mensaje) {
    document.getElementById('mensaje').innerText = mensaje;
}

// Función que maneja el evento submit del formulario
function manejarFormulario(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado del formulario

    const correo = document.getElementById('mail_username').value;
    const password = document.getElementById('password_sfa').value;

    // Llamada a la función que envía el formulario y maneja la respuesta
    enviarFormulario(correo, password)
        .then(data => {
            if (data) {
                mostrarMensaje(`Respuesta: ${data.mensaje}`);
            } else {
                mostrarMensaje('Error al conectar con el servidor');
            }
        });
}

// Asignar el evento al formulario cuando la página se cargue
document.getElementById('login-form').addEventListener('submit', manejarFormulario);




//DE AQUÍ PARA ABAJO ES LO QUE APRENDÍ DE JavaScript en coursera gcs a Dios

/*var x = "Poco a poco, despacio llegarán más lejos! JESUS";
x = x + ". JESUS JOSE Y MARIA en sus manos pongo el alma mía";

console.log(x + "!!!");

//object creation
var company = new Object();
company.name = "Dios";
company.idea = new Object();
company.idea.descripcion = "Santidad";

console.log(company);
console.log(company.idea);
console.log(company["idea"]);



// Better way: object literal
var facebook = {
  name: "Facebook",
  ceo: {
    firstName: "Mark",
    favColor: "blue"
  },
  "stock of company": 110
};

console.log(facebook.ceo.firstName);



#html anterior:

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
  </head>
<body>
  <h1>Lecture 40</h1>

  <script src="js/script.js"></script>
  <script>
  console.log(x);
  </script>
</body>
</html>
*/