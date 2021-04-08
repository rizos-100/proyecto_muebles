function decidirCategoria(){
    if($('#txtIdCategoria').val() == ""){
        agregarCategoria();
    }else{
        modificarCategoria();
    }
}

function agregarCategoria(){
    if(validarCategoria()){
        var data = {
            nombre: $('#txtNombreCategoria').val(),
            descripcion: $('#txtDescCategoria').val()
        };
        $.ajax(
                {
                    type: "POST",
                    url: "/addCategoria",
                    async: true,
                    data: data
                })
                .done(
                        function (data) {
                            Swal.fire('Movimiento realizado', 'Categoria guardada con exito', 'success');
                            setTimeout(function(){location.href ="/getAllCategoriasActivas";;},2000)
                        }
                );
    }else{
        Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
    }
    
}

function modificarCategoria(){
    if(validarCategoria()){
        var data = {
            id: $('#txtIdCategoria').val(),
            nombre: $('#txtNombreCategoria').val(),
            descripcion: $('#txtDescCategoria').val()
        };
        $.ajax(
                {
                    type: "POST",
                    url: "/updateCategoria",
                    async: true,
                    data: data
                })
                .done(
                        function (data) {
                            Swal.fire('Movimiento realizado', 'Categoria modificada con exito', 'success');
                            setTimeout(function(){location.href ="/getAllCategoriasActivas";;},2000)
                        }
                );
    }else{
        Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
    }
    
}

function detalleCategoria(idC){
    var data = {
        idCat: idC
    };
    $.ajax(
            {
                type: "Get",
                url: "/getCategoriasPorId",
                async: true,
                data: data
            })
            .done(
                    function (data) {
                        categoria = data;
                        $('#txtIdCategoria').val(categoria.id);
                        $('#txtNombreCategoria').val(categoria.nombre);
                        $('#txtDescCategoria').val(categoria.descripcion);
                        $('#modalCategoria').modal('show');
                    }
            );
    
}

function eliminarCategoria(idC){
    Swal.fire({
        title: '¿Seguro que deseas eliminarlo?',
        text: "Es posible que no puedas deshacerlo!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, Eliminar!',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.value) {
            var data = {
                id: idC
            };
            $.ajax(
                    {
                        type: "POST",
                        url: "/deleteCategoria",
                        async: true,
                        data: data
                    })
                    .done(
                            function (data) {
                                Swal.fire('Movimiento realizado', 'Categoria eliminada con exito', 'success');
                                setTimeout(function(){location.href ="/getAllCategoriasInactivas";},2000)
                            }
                    );
        }
    });
    
}

function validarCategoria(){
    if($('#txtNombreCategoria').val() == ""){
        return false;
    }
    if($('#txtDescCategoria').val() == ""){
        return false;
    }
    return true;
}