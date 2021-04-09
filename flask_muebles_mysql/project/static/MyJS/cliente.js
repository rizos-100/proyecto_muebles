function decidirCliente(){
    if($('#txtIdCategoria').val() == ""){
        agregarCliente();
    }else{
        modificarCliente();
    }
}

function agregarCliente(){
    var err = validarCliente();
    if(err == "ok"){
        alert("Aqui");
        var data = {
            nombre: $('#txtNombreCategoria').val(),
            descripcion: $('#txtDescCategoria').val()
        };

        swal({
            title: "¿Deseas continuar?",
            text: "Por favor, confirma que deseas agregar el registro.",
            type: "info",
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonColor: "#4caf50",
            confirmButtonText: "Si, agregar",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax(
                {
                    type: "POST",
                    url: "/addCategoria",
                    async: true,
                    data: data
                })
                .done(
                        function (data) {
                            swal("Correcto", "Categoría guardada con exíto. ", "success");
                            setTimeout(function(){location.href ="/getAllCategoriasActivas";;},2000)
                        }
                );
        });
    }else{
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-black", err, "bottom", "left", "", "");
    }
    
}

function modificarCliente(){
    var err = validarCliente();
    if(err == "ok"){
        var data = {
            id: $('#txtIdCategoria').val(),
            nombre: $('#txtNombreCategoria').val(),
            descripcion: $('#txtDescCategoria').val()
        };
        swal({
            title: "¿Deseas continuar?",
            text: "Por favor, confirma que deseas modificar el registro.",
            type: "info",
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonColor: "#4caf50",
            confirmButtonText: "Si, modificar",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax(
                {
                    type: "POST",
                    url: "/updateCategoria",
                    async: true,
                    data: data
                })
                .done(
                        function (data) {
                            swal('Movimiento realizado', 'Categoría modificada con exíto', 'success');
                            setTimeout(function(){location.href ="/getAllCategoriasActivas";;},2000)
                        }
                );
        });
    }else{
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-black", err, "bottom", "left", "", "");
    }
    
}

function detalleCliente(idC){
    var data = {
        idCliente: idC
    };
    $.ajax(
            {
                type: "GET",
                url: "/getAllClientesById",
                async: true,
                data: data
            })
            .done(
                    function (data) {
                        cliente = data;
                        $('#txtNombre').val(cliente.persona.nombre);
                        $('#txtApellidoPaterno').val(cliente.persona.apellidoP);
                        $('#txtApellidoMaterno').val(cliente.persona.apellidoM);
                        $('#txtRFC').val(cliente.persona.rfc);
                        $('#txtNumeroFijo').val(cliente.persona.numFijo);
                        $('#txtNumeroCelular').val(cliente.persona.celular);
                        $('#txtCalle').val(cliente.domicilio.calle);
                        $('#txtNumeroExterior').val(cliente.domicilio.numero_exterior);
                        $('#txtNumeroInterior').val(cliente.domicilio.numero_interior);
                        $('#txtColonia').val(cliente.domicilio.colonia);
                        $('#txtCP').val(cliente.domicilio.cp);
                        $('#txtMunicipio').val(cliente.domicilio.municipio);
                        $('#txtEstado').val(cliente.domicilio.estado);
                        $('#txtReferencias').val(cliente.domicilio.referencias);
                        $('#txtIdCliente').val(cliente.idCliente);
                        $('#txtIdPersona').val(cliente.persona.id);
                        $('#txtIdDomicilio').val(cliente.domicilio.id);
                        $('#modalCliente').modal('show');
                    }
            );
    
}

function eliminarCliente(idPe){
    var data = {
        idP: idPe
    };
    swal({
        title: "¿Deseas continuar?",
        text: "Por favor, confirma que deseas eliminar el registro.",
        type: "info",
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, eliminar",
        closeOnConfirm: false,
        showLoaderOnConfirm: true
    }, function () {
        $.ajax(
            {
                type: "POST",
                url: "/deleteCliente",
                async: true,
                data: data
            })
            .done(
                    function (data) {
                        swal('Movimiento realizado', 'Cliente eliminado con exíto.', 'success');
                        setTimeout(function(){location.href ="/getAllClientesInactivos";},2000)
                    }
            );
    });
    
}

function validarCliente(){
    if($('#txtNombreCategoria').val() == ""){
        return "Por favor, indica el nombre. ";
    }

    if($('#txtDescCategoria').val() == ""){
        return "Por favor, indica la descripción";;
    }

    return "ok";
}



/* Funciones para notificaciones */

function showNotification(colorName, text, placementFrom, placementAlign, animateEnter, animateExit) {
    if (colorName === null || colorName === '') {
        colorName = 'bg-black';
    }
    if (text === null || text === '') {
        text = 'Turning standard Bootstrap alerts';
    }
    if (animateEnter === null || animateEnter === '') {
        animateEnter = 'animated fadeInDown';
    }
    if (animateExit === null || animateExit === '') {
        animateExit = 'animated fadeOutUp';
    }
    var allowDismiss = true;

    $.notify({
        message: text
    },
            {
                type: colorName,
                allow_dismiss: allowDismiss,
                newest_on_top: true,
                timer: 1000,
                placement: {
                    from: placementFrom,
                    align: placementAlign
                },
                animate: {
                    enter: animateEnter,
                    exit: animateExit
                },
                template: '<div data-notify="container" class="bootstrap-notify-container alert alert-dismissible {0} ' + (allowDismiss ? "p-r-35" : "") + '" role="alert">' +
                        '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                        '<span data-notify="icon"></span> ' +
                        '<span data-notify="title">{1}</span> ' +
                        '<span data-notify="message">{2}</span>' +
                        '<div class="progress" data-notify="progressbar">' +
                        '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                        '</div>' +
                        '<a href="{3}" target="{4}" data-notify="url"></a>' +
                        '</div>'
            });
}