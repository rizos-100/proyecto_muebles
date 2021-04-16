function decidirEmpleado() {
    if ($('#txtIdPersonaE').val() == "") {
        agregarEmpleado();
    } else {
        modificarEmpleado();
    }
}

function agregarEmpleado() {
    var err = validarEmpleado();
    if (err == "ok") {
        var data = {
            nombre: validarCamposLetras($('#txtNombreE').val()),
            apellidoP: validarCamposLetras($('#txtApellidoPaternoE').val()),
            apellidoM: validarCamposLetras($('#txtApellidoMaternoE').val()),
            rfc: validarCamposLetras($('#txtRFCE').val()),
            numero_fijo: validarCamposLetras($('#txtNumeroFijoE').val()), 
            celular: validarCamposLetras($('#txtNumeroCelularE').val()), 
            calle: validarCamposLetras($('#txtCalleE').val()),
            numero_exterior: validarCamposLetras($('#txtNumeroExteriorE').val()),
            numero_interior: validarCamposLetras($('#txtNumeroInteriorE').val()), 
            colonia: validarCamposLetras($('#txtColoniaE').val()),
            cp: validarCamposLetras($('#txtCPE').val()),
            municipio: validarCamposLetras($('#txtMunicipioE').val()),
            estado: validarCamposLetras($('#txtEstadoE').val()),
            referencias: validarCamposLetras($('#txtReferenciasE').val())
        };

        console.log(data);

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
                    url: "/addEmpleado",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Empleado guardado con exíto. ", "success");
                        setTimeout(function () { location.href = "/getAllEmpleadosSinAsignar";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function modificarEmpleado() {
    var err = validarEmpleado();
    if (err == "ok") {
        var data = {
            idP: $('#txtIdPersonaE').val(),
            idD: $('#txtIdDomicilioE').val(),
            nombre: validarCamposLetras($('#txtNombreE').val()),
            apellidoP: validarCamposLetras($('#txtApellidoPaternoE').val()),
            apellidoM: validarCamposLetras($('#txtApellidoMaternoE').val()),
            rfc: validarCamposLetras($('#txtRFCE').val()),
            numero_fijo: validarCamposLetras($('#txtNumeroFijoE').val()), 
            celular: validarCamposLetras($('#txtNumeroCelularE').val()), 
            calle: validarCamposLetras($('#txtCalleE').val()),
            numero_exterior: validarCamposLetras($('#txtNumeroExteriorE').val()),
            numero_interior: validarCamposLetras($('#txtNumeroInteriorE').val()), 
            colonia: validarCamposLetras($('#txtColoniaE').val()),
            cp: validarCamposLetras($('#txtCPE').val()),
            municipio: validarCamposLetras($('#txtMunicipioE').val()),
            estado: validarCamposLetras($('#txtEstadoE').val()),
            referencias: validarCamposLetras($('#txtReferenciasE').val())
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
                    url: "/updateEmpleado",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal('Movimiento realizado', 'Empleado modificado con exíto', 'success');
                        setTimeout(function () { location.href = "/getAllEmpleadosSinAsignar";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function detalleEmpleado(idP) {
    var data = {
        idPersona: idP
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllEmpleadosById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                persona = data;
                console.log(persona);
                $('#txtNombreE').val(persona.nombre);
                $('#txtApellidoPaternoE').val(persona.apellidoP);
                $('#txtApellidoMaternoE').val(persona.apellidoM);
                $('#txtRFCE').val(persona.rfc);
                $('#txtNumeroFijoE').val(persona.numero_fijo);
                $('#txtNumeroCelularE').val(persona.celular);
                $('#txtCalleE').val(persona.domicilio.calle);
                $('#txtNumeroExteriorE').val(persona.domicilio.numero_exterior);
                $('#txtNumeroInteriorE').val(persona.domicilio.numero_interior);
                $('#txtColoniaE').val(persona.domicilio.colonia);
                $('#txtCPE').val(persona.domicilio.cp);
                $('#txtMunicipioE').val(persona.domicilio.municipio);
                $('#txtEstadoE').val(persona.domicilio.estado);
                $('#txtReferenciasE').val(persona.domicilio.referencias);
                $('#txtIdPersonaE').val(persona.id);
                $('#txtIdDomicilioE').val(persona.domicilio.id);
                $('#modalEmpleado').modal('show');
            }
        );

}

function eliminarEmpleado(idP) {
    var data = {
        idP: idP
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
                url: "/deleteEmpleado",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Empleado eliminado con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllEmpleadosSinAsignar"; }, 2000)
                }
            );
    });

}

function validarEmpleado() {
    if ($('#txtNombreE').val() == "") {
        return "Por favor, indica el nombre. ";
    }
    if ($('#txtApellidoPaternoE').val() == "") {
        return "Por favor, indica el apellido paterno. ";;
    }
    if ($('#txtApellidoMaternoE').val() == "") {
        return "Por favor, indica el apellido materno. ";
    }
    if ($('#txtRFCE').val() == "") {
        return "Por favor, indica el RFC. ";;
    }
    if ($('#txtNumeroFijEo').val() == "") {
        return "Por favor, indica el número fijo. ";
    }
    if ($('#txtNumeroCelularE').val() == "") {
        return "Por favor, indica el número celular. ";;
    }
    if ($('#txtCalleE').val() == "") {
        return "Por favor, indica la calle. ";
    }
    if ($('#txtColoniaE').val() == "") {
        return "Por favor, indica la colonia. ";
    }
    if ($('#txtNumeroExteriorE').val() == "") {
        return "Por favor, indica el número exterior. ";
    }
    if ($('#txtNumeroInteriorE').val() == "") {
        return "Por favor, indica el número interior. ";
    }
    if ($('#txtCPE').val() == "") {
        return "Por favor, indica el código postal. ";;
    }
    if ($('#txtMunicipioE').val() == "") {
        return "Por favor, indica el municipio. ";
    }
    if ($('#txtEstadoE').val() == "") {
        return "Por favor, indica el estado";;
    }
    if ($('#txtReferenciasE').val() == "") {
        return "Por favor, indica las referencias.";;
    }
    
    return "ok";
}

function limpiarEmpleado() {
    $('#txtNombreE').val('');
    $('#txtApellidoPaternoE').val('');
    $('#txtApellidoMaternoE').val('');
    $('#txtRFCE').val('');
    $('#txtNumeroFijoE').val('');
    $('#txtNumeroCelularE').val('');
    $('#txtCalleE').val('');
    $('#txtNumeroExteriorE').val('');
    $('#txtNumeroInteriorE').val('');
    $('#txtColoniaE').val('');
    $('#txtCPE').val('');
    $('#txtMunicipioE').val('');
    $('#txtEstadoE').val('');
    $('#txtReferenciasE').val('');
    $('#txtIdPersonaE').val('');
    $('#txtIdDomicilioE').val('');
}

function detalleEmpleadoModificar(idP) {
    var data = {
        idPersona: idP
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllEmpleadosById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                persona = data;
                $('#txtNombreE').val(persona.nombre);
                $('#txtApellidoPaternoE').val(persona.apellidoP);
                $('#txtApellidoMaternoE').val(persona.apellidoM);
                $('#txtRFCE').val(persona.rfc);
                $('#txtNumeroFijoE').val(persona.numero_fijo);
                $('#txtNumeroCelularE').val(persona.celular);
                $('#txtCalleE').val(persona.domicilio.calle);
                $('#txtNumeroExteriorE').val(persona.domicilio.numero_exterior);
                $('#txtNumeroInteriorE').val(persona.domicilio.numero_interior);
                $('#txtColoniaE').val(persona.domicilio.colonia);
                $('#txtCPE').val(persona.domicilio.cp);
                $('#txtMunicipioE').val(persona.domicilio.municipio);
                $('#txtEstadoE').val(persona.domicilio.estado);
                $('#txtReferenciasE').val(persona.domicilio.referencias);
                $('#txtIdPersonaE').val(persona.id);
                $('#txtIdDomicilioE').val(persona.domicilio.id);
                $('#modalEmpleadoModificar').modal('show');
            }
        );

}

function modificarEmpleadoModificar() {
    var err = validarEmpleado();
    if (err == "ok") {
        var data = {
            idP: $('#txtIdPersonaE').val(),
            idD: $('#txtIdDomicilioE').val(),
            nombre: validarCamposLetras($('#txtNombreE').val()),
            apellidoP: validarCamposLetras($('#txtApellidoPaternoE').val()),
            apellidoM: validarCamposLetras($('#txtApellidoMaternoE').val()),
            rfc: validarCamposLetras($('#txtRFCE').val()),
            numero_fijo: validarCamposLetras($('#txtNumeroFijoE').val()), 
            celular: validarCamposLetras($('#txtNumeroCelularE').val()), 
            calle: validarCamposLetras($('#txtCalleE').val()),
            numero_exterior: validarCamposLetras($('#txtNumeroExteriorE').val()),
            numero_interior: validarCamposLetras($('#txtNumeroInteriorE').val()), 
            colonia: validarCamposLetras($('#txtColoniaE').val()),
            cp: validarCamposLetras($('#txtCPE').val()),
            municipio: validarCamposLetras($('#txtMunicipioE').val()),
            estado: validarCamposLetras($('#txtEstadoE').val()),
            referencias: validarCamposLetras($('#txtReferenciasE').val())
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
                    url: "/updateEmpleado",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal('Movimiento realizado', 'Empleado modificado con exíto', 'success');
                        setTimeout(function () { location.href = "/getAllEmpleadosActivos";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function eliminarEmpleadoModificar(idP) {
    var data = {
        idP: idP
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
                url: "/deleteEmpleado",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Empleado eliminado con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllEmpleadosInactivos"; }, 2000)
                }
            );
    });

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
            z_index: 1500,
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