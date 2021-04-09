function decidirProveedor(){
    if ($('#txtIdProveedor').val() == "") {
        agregarProveedor();
    } else {
        modificarProveedor();
    }
}

function agregarProveedor() {
    var err = validarProveedor();
    if (err == "ok") {
        var data = {
            nombre: validarCamposLetras($('#txtNombreProveedor').val()),
            rfc: validarCamposLetras($('#txtRFCProveedor').val()),
            nombre_contacto: validarCamposLetras($('#txtNombreContacto').val()),
            puesto_contacto: validarCamposLetras($('#txtPuestoContacto').val()),
            telefono_contacto: validarCamposLetras($('#txtTelefonoContacto').val()), 
            correo_contacto: validarCamposLetras($('#txtCorreoContacto').val()), 
            calle: validarCamposLetras($('#txtCalleP').val()),
            num_ext: validarCamposLetras($('#txtNumeroExteriorP').val()),
            num_int: validarCamposLetras($('#txtNumeroInteriorP').val()), 
            colonia: validarCamposLetras($('#txtColoniaP').val()),
            cp: validarCamposLetras($('#txtCPP').val()),
            municipio: validarCamposLetras($('#txtMunicipioP').val()),
            estado: validarCamposLetras($('#txtEstadoP').val()),
            referencias: validarCamposLetras($('#txtReferenciasP').val())
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
                    url: "/addProveedor",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Proveedor guardado con exíto. ", "success");
                        setTimeout(function () { location.href = "/getAllProveedorActivos";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function modificarProveedor() {
    var err = validarProveedor();
    if (err == "ok") {
        var data = {
            id: $('#txtIdProveedor').val(),
            idDomicilio: $('#txtIdDomicilioP').val(),
            nombre: validarCamposLetras($('#txtNombreProveedor').val()),
            rfc: validarCamposLetras($('#txtRFCProveedor').val()),
            nombre_contacto: validarCamposLetras($('#txtNombreContacto').val()),
            puesto_contacto: validarCamposLetras($('#txtPuestoContacto').val()),
            telefono_contacto: validarCamposLetras($('#txtTelefonoContacto').val()), 
            correo_contacto: validarCamposLetras($('#txtCorreoContacto').val()), 
            calle: validarCamposLetras($('#txtCalleP').val()),
            num_ext: validarCamposLetras($('#txtNumeroExteriorP').val()),
            num_int: validarCamposLetras($('#txtNumeroInteriorP').val()), 
            colonia: validarCamposLetras($('#txtColoniaP').val()),
            cp: validarCamposLetras($('#txtCPP').val()),
            municipio: validarCamposLetras($('#txtMunicipioP').val()),
            estado: validarCamposLetras($('#txtEstadoP').val()),
            referencias: validarCamposLetras($('#txtReferenciasP').val())
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
                    url: "/updateProveedor",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal('Movimiento realizado', 'Proveedor modificado con exíto', 'success');
                        setTimeout(function () { location.href = "/getAllProveedorActivos";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function detalleProveedor(idP) {
    var data = {
        idProveedor: idP
    };
    $.ajax(
        {
            type: "POST",
            url: "/getAllProveedorById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                proveedor = data;
                console.log(proveedor)
                $('#txtNombreProveedor').val(proveedor.nombre);
                $('#txtRFCProveedor').val(proveedor.rfc);
                $('#txtNombreContacto').val(proveedor.nombre_contacto);
                $('#txtPuestoContacto').val(proveedor.puesto_contacto);
                $('#txtTelefonoContacto').val(proveedor.telefono_contacto);
                $('#txtCorreoContacto').val(proveedor.correo_contacto);
                $('#txtCalleP').val(proveedor.domicilio.calle);
                $('#txtNumeroExteriorP').val(proveedor.domicilio.num_ext);
                $('#txtNumeroInteriorP').val(proveedor.domicilio.num_int);
                $('#txtColoniaP').val(proveedor.domicilio.colonia);
                $('#txtCPP').val(proveedor.domicilio.cp);
                $('#txtMunicipioP').val(proveedor.domicilio.municipio);
                $('#txtEstadoP').val(proveedor.domicilio.estado);
                $('#txtReferenciasP').val(proveedor.domicilio.referencias);
                $('#txtIdProveedor').val(proveedor.id);
                $('#txtIdDomicilioP').val(proveedor.domicilio.idD);
                $('#modalProveedor').modal('show');
            }
        );

}

function eliminarProveedor(idP) {
    var data = {
        id: idP
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
                url: "/deleteProveedor",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Proveedor eliminado con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllProveedorInactivos"; }, 2000)
                }
            );
    });

}

function validarProveedor() {
    if ($('#txtNombreProveedor').val() == "") {
        return "Por favor, indica el nombre de la empresa. ";
    }
    if ($('#txtRFCProveedor').val() == "") {
        return "Por favor, indica el RFC. ";;
    }
    if ($('#txtNombreContacto').val() == "") {
        return "Por favor, indica el nombre del contacto. ";
    }
    if ($('#txtPuestoContacto').val() == "") {
        return "Por favor, indica el puesto del contacto. ";;
    }
    if ($('#txtTelefonoContacto').val() == "") {
        return "Por favor, indica el teléfono del contacto. ";
    }
    if ($('#txtCorreoContacto').val() == "") {
        return "Por favor, indica el correo del contacto. ";;
    }
    if ($('#txtCalleP').val() == "") {
        return "Por favor, indica la calle. ";
    }
    if ($('#txtColoniaP').val() == "") {
        return "Por favor, indica la colonia. ";
    }
    if ($('#txtNumeroExteriorP').val() == "") {
        return "Por favor, indica el número exterior. ";
    }
    if ($('#txtNumeroInteriorP').val() == "") {
        return "Por favor, indica el número interior. ";
    }
    if ($('#txtCPP').val() == "") {
        return "Por favor, indica el código postal. ";;
    }
    if ($('#txtMunicipioP').val() == "") {
        return "Por favor, indica el municipio. ";
    }
    if ($('#txtEstadoP').val() == "") {
        return "Por favor, indica el estado";;
    }
    if ($('#txtReferenciasP').val() == "") {
        return "Por favor, indica las referencias.";;
    }
    
    return "ok";
}

function limpiarProveedor() {
    $('#txtNombreProveedor').val('');
    $('#txtRFCProveedor').val('');
    $('#txtNombreContacto').val('');
    $('#txtPuestoContacto').val('');
    $('#txtTelefonoContacto').val('');
    $('#txtCorreoContacto').val('');
    $('#txtCalleP').val('');
    $('#txtNumeroExteriorP').val('');
    $('#txtNumeroInteriorP').val('');
    $('#txtColoniaP').val('');
    $('#txtCPP').val('');
    $('#txtMunicipioP').val('');
    $('#txtEstadoP').val('');
    $('#txtReferenciasP').val('');
    $('#txtIdProveedor').val('');
    $('#txtIdDomicilioP').val('');
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