function decidirCategoria() {
    if ($('#txtIdCategoria').val() == "") {
        agregarCategoria();
    } else {
        modificarCategoria();
    }
}

function agregarCategoria() {
    var err = validarCategoria();
    if (err == "ok") {
        var data = {
            nombre: validarCamposLetras($('#txtNombreCategoria').val()),
            descripcion: validarCamposLetras($('#txtDescCategoria').val())
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
                        setTimeout(function () { location.href = "/getAllCategoriasActivas";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function modificarCategoria() {
    var err = validarCategoria();
    if (err == "ok") {
        var data = {
            id: $('#txtIdCategoria').val(),
            nombre: validarCamposLetras($('#txtNombreCategoria').val()),
            descripcion: validarCamposLetras($('#txtDescCategoria').val())
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
                        setTimeout(function () { location.href = "/getAllCategoriasActivas";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function detalleCategoria(idC) {
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

function eliminarCategoria(idC) {
    var data = {
        id: idC
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
                url: "/deleteCategoria",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Categoría eliminada con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllCategoriasInactivas"; }, 2000)
                }
            );
    });

}

function validarCategoria() {
    if ($('#txtNombreCategoria').val() == "") {
        return "Por favor, indica el nombre. ";
    }

    if ($('#txtDescCategoria').val() == "") {
        return "Por favor, indica la descripción";;
    }

    return "ok";
}

function limpiarCategoria() {
    $('#txtIdCategoria').val('');
    $('#txtNombreCategoria').val('');
    $('#txtDescCategoria').val('');
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