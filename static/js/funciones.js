function agregarBebida(){
    document.getElementById("formulario").action="addBebida"
}

function consultarEst(){
    document.getElementById("formulario").action="estudiante/get"
}

function listarEst(){
    document.getElementById("formulario").action="estudiante/list"
}

function actualizarEst(){
    document.getElementById("formulario").action="estudiante/update"
}

function eliminarEst(){
    document.getElementById("formulario").action="estudiante/delete"
}