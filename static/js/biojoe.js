function validar_formulario(){
    let username = document.formRegistro.username;
    let email = document.formRegistro.email;
    let password = document.formRegistro.password;
    let password2 = document.formRegistro.password2;

    let username_len = username.value.length;

    //if(username_len == 0 || username_len < 8){
    //    alert("Debes ingresar un username con minímo 8 caracteres");
    //    username_len.focus(); // No debe borrar los datos.
    //    return false;
    //}

    let formato_email = /^\w+([\.-]?\w+)@\w+([\.-]?\w+)(\.\w{2,3})+$/;
    if(!email.value.match(formato_email)){
        alert("Debes ingresar un email valido!");
        email.focus();
        return false;
    }

    let pass_len = password.value.length;
    if( pass_len == 0 || pass_len < 8){
        alert("Debes ingresar un password con más de 8 caracteres");
        return false;
    }

    if ( password.value != password2.value){

        alert("El password no coincide, el password debe ser igual en ambos campos!")
        return false;
    }
    
}

// Muestra la clave al pasar el mouse sobre la etiqueta img.
function mostrarPassword(obj){
    var obj = document.getElementById("password");
    obj.type="text";
}

function ocultarPassword(obj){
    var obj = document.getElementById("password");
    obj.type="password";
}
