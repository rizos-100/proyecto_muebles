function decidirMaterial() {
    if ($('#txtIdMaterial').val() == "") {
        agregarMaterial();
    } else {
        modificarMaterial();
    }
}

function agregarMaterial() {
    var err = validarMaterial();
    if (err == "ok") {
        var data = {
            tipo: validarCamposLetras($('#lstTipoM').val()),
            nombre: validarCamposLetras($('#txtNombreMaterial').val()),
            descripcion: validarCamposLetras($('#txtDescripcionMaterial').val()),
            cantidad: validarCamposLetras($('#txtCantidadMaterial').val()),
            alto: validarCamposLetras($('#txtAltoMaterial').val()),
            ancho: validarCamposLetras($('#txtAnchoMaterial').val()), 
            grosor: validarCamposLetras($('#txtGrosorMaterial').val()), 
            color: validarCamposLetras($('#txtColorMaterial').val())
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
                    url: "/addMaterial",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Material guardado con exíto. ", "success");
                        setTimeout(function () { location.href = "/getAllMaterialDisponibles"; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function modificarMaterial() {
    var err = validarMaterial();
    if (err == "ok") {
        var data = {
            id: $('#txtIdMaterial').val(),
            tipo: validarCamposLetras($('#lstTipoM').val()),
            nombre: validarCamposLetras($('#txtNombreMaterial').val()),
            descripcion: validarCamposLetras($('#txtDescripcionMaterial').val()),
            cantidad: validarCamposLetras($('#txtCantidadMaterial').val()),
            alto: validarCamposLetras($('#txtAltoMaterial').val()),
            ancho: validarCamposLetras($('#txtAnchoMaterial').val()), 
            grosor: validarCamposLetras($('#txtGrosorMaterial').val()), 
            color: validarCamposLetras($('#txtColorMaterial').val())
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
                    url: "/updateMaterial",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal('Movimiento realizado', 'Material modificado con exíto', 'success');
                        setTimeout(function () { location.href = "/getAllMaterialDisponibles"; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function detalleTablaM(idM) {
    var data = {
        id: idM
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllMaterialPorId",
            async: true,
            data: data
        })
        .done(
            function (data) {
                Material = data;
                $('#txtIdMaterial').val(Material.id);
                $('#txtNombreMaterial').val(Material.nombre);
                $('#txtDescripcionMaterial').val(Material.descripcion);
                $('#txtCantidadMaterial').val(Material.cantidad);
                $('#txtAltoMaterial').val(Material.alto);
                $('#txtAnchoMaterial').val(Material.ancho);
                $('#txtGrosorMaterial').val(Material.grosor);
                $('#txtColorMaterial').val(Material.color);
                $('#modalMaterial').modal('show');
            }
        );

}

function eliminarMaterial(idM) {
    var data = {
        id: idM
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
                url: "/deleteMaterial",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Material eliminado con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllMaterialDisponibles"; }, 2000)
                }
            );
    });

}

function validarMaterial() {
    console.log($('#lstTipoM').val())
    if ($('#lstTipoM').val() == null) {
        return "Por favor, selecciona el tipo de material. ";
    }else{
        if ($('#txtNombreMaterial').val() == "") {
            return "Por favor, indica el nombre. ";
        }
        if ($('#txtDescripcionMaterial').val() == "") {
            return "Por favor, indica la descripción. ";;
        }
        if ($('#txtCantidadMaterial').val() == "") {
            return "Por favor, indica la cantidad. ";
        }
        if ($('#lstTipoM').val() == "Tabla") {
            if ($('#txtAltoMaterial').val() == "") {
                return "Por favor, indica el alto. ";
            }
            if ($('#txtAnchoMaterial').val() == "") {
                return "Por favor, indica el ancho. ";;
            }
            if ($('#txtGrosorMaterial').val() == "") {
                return "Por favor, indica el grosor. ";
            }
        }
        if ($('#lstTipoM').val() == "Tornillo") {
            if ($('#txtAltoMaterial').val() == "") {
                return "Por favor, indica el alto. ";
            }
        }
        if ($('#lstTipoM').val() == "Clavo") {
            if ($('#txtAltoMaterial').val() == "") {
                return "Por favor, indica el alto. ";
            }
        }
        if ($('#lstTipoM').val() == "Riel") {
            if ($('#txtAltoMaterial').val() == "") {
                return "Por favor, indica el alto. ";
            }
        }
        if ($('#lstTipoM').val() == "Pintura") {
            if ($('#txtColorMaterial').val() == "") {
                return "Por favor, indica el color. ";
            }
        }
        if ($('#lstTipoM').val() == "Agarradera") {
            if ($('#txtAnchoMaterial').val() == "") {
                return "Por favor, indica el ancho. ";;
            }
        }
        if ($('#lstTipoM').val() == "Escuadra") {
            if ($('#txtAltoMaterial').val() == "") {
                return "Por favor, indica el alto. ";
            }
            if ($('#txtAnchoMaterial').val() == "") {
                return "Por favor, indica el ancho. ";;
            }
        }
    }
    
    return "ok";
}

function limpiarMaterial() {
    $('#txtIdMaterial').val('');
    $('#txtNombreMaterial').val('');
    $('#txtDescripcionMaterial').val('');
    $('#txtCantidadMaterial').val('');
    $('#txtAltoMaterial').val('');
    $('#txtAnchoMaterial').val('');
    $('#txtGrosorMaterial').val('');
    $('#txtColorMaterial').val('');
    ocultarCampos();
}

function ocultarCampos() {
    $('#divTiposM').hide();
    $('#divAlto').hide();
    $('#divAncho').hide();
    $('#divGrosor').hide();
    $('#divColor').hide();
}

function mostrarCampos() {
    $('#divTiposM').show();
    if ($('#lstTipoM').val() == "Tabla") {
        $('#divAlto').show();
        $('#divAncho').show();
        $('#divGrosor').show();
    }
    if ($('#lstTipoM').val() == "Tornillo") {
        $('#divAlto').show();
    }
    if ($('#lstTipoM').val() == "Clavo") {
        $('#divAlto').show();
    }
    if ($('#lstTipoM').val() == "Riel") {
        $('#divAlto').show();
    }
    if ($('#lstTipoM').val() == "Pintura") {
        $('#divColor').show();
    }
    if ($('#lstTipoM').val() == "Agarradera") {
        $('#divAncho').show();
    }
    if ($('#lstTipoM').val() == "Escuadra") {
        $('#divAlto').show();
        $('#divAncho').show();
    }
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