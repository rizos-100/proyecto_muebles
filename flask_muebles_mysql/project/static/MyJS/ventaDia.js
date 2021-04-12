var productos = [];
var productos_envio = [];
var cliente = "";

function seleccionarCliente(idC) {
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
                swal({
                    title: "¿Deseas continuar?",
                    text: "Por favor, confirma que deseas agregar el cliente a la venta.",
                    type: "info",
                    showCancelButton: true,
                    cancelButtonText: 'Cancelar',
                    confirmButtonColor: "#4caf50",
                    confirmButtonText: "Si, agregar",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: false
                }, function () {
                    swal("Correcto", "Cliente agregado a la venta. ", "success");
                    $('#txtNombreClienteVenta').text(cliente.persona.nombre + ' ' + cliente.persona.apellidoP + ' ' + cliente.persona.apellidoM);
                    $('#txtIdClienteAV').val(cliente.idCliente);
                    $('#modalClienteV').modal('hide');
                });

            }
        );

}

function seleccionarProducto(idP) {
    var data = {
        id: idP
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllProductosPorId",
            async: true,
            data: data
        })
        .done(
            function (data) {
                producto = data;
                var cantidad = parseInt($('#txtCantidadProducto').val());
                //console.log(producto);
                if (cantidad <= parseInt(producto.cantidad)) {
                    swal({
                        title: "¿Deseas continuar?",
                        text: "Por favor, confirma que deseas agregar el producto.",
                        type: "info",
                        showCancelButton: true,
                        cancelButtonText: 'Cancelar',
                        confirmButtonColor: "#4caf50",
                        confirmButtonText: "Si, agregar",
                        closeOnConfirm: false,
                        showLoaderOnConfirm: false
                    }, function () {

                        var subtotal = cantidad * parseFloat(producto.precio);

                        var parametros = {
                            "img": producto.img,
                            "modelo": producto.modelo,
                            "descripcion": producto.descripcion,
                            "producto": producto.idProducto,
                            "cantidad": cantidad,
                            "subtotal": Math.round(subtotal)
                        };

                        var parametros_envio = {
                            "producto": producto.idProducto,
                            "cantidad": cantidad,
                            "subtotal": Math.round(subtotal)
                        };

                        productos.push(parametros);
                        productos_envio.push(parametros_envio);
                        llenarTablaDetalleProducto();
                        swal("Correcto", "Producto agregado a la venta. ", "success");
                        $('#modalProductoV').modal('hide');
                    });
                }
                else {
                    showNotification("bg-red", "La cantidad ingresada no se tiene en almacén. ", "bottom", "right", "", "");
                }

            }
        );
}

function eliminarProductoVenta(indice) {
    swal({
        title: "¿Deseas continuar?",
        text: "Por favor, confirma que deseas eliminar el registro.",
        type: "info",
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, eliminar",
        closeOnConfirm: false,
        showLoaderOnConfirm: false
    }, function () {
        productos.splice(indice, 1);
        swal("Correcto", "Producto eliminado de la venta. ", "success");
        llenarTablaDetalleProducto();
    });
}

function llenarTablaDetalleProducto() {
    var datos = "";
    var total = 0;
    if (productos.length === 0) {
        datos += '<tr>';
        datos += '<td> No hay registros para mostrar</td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '</tr>';
        $('#tbodyVentaAgregarProducto').html(datos);
    } else {
        $("#tbVentaAgregarProducto > tbody").empty();
        for (var i = 0; i < productos.length; i++) {
            total = total + Math.round(productos[i]["subtotal"]);
            //console.log(productos[i]["subtotal"]);
            $("#tbVentaAgregarProducto>tbody").append('<tr><td class="text-center"> <img class="mb-4" src="'+ productos[i]["img"] + '" alt="" width="120" height="95"></td><td>' + productos[i]["modelo"] + '</td><td>' + productos[i]["descripcion"] + '</td><td>' + productos[i]["cantidad"] + '</td><td>' + Math.round(productos[i]["subtotal"]) + '</td><td class="text-center"> <button type="button" class="btn btn-danger waves-effect" onclick="eliminarProductoVenta(' + i + ')"> <i class="material-icons">delete</i></button> </td></tr>');
        }
        $('#txtTotalVentaAgregar').text(total);
    }
}

function agregarVenta() {
    var err = validarVenta();
    if (err == "ok") {
        var data = {
            total: parseInt($('#txtTotalVentaAgregar').text()),
            cliente: cliente.idCliente,
            user: localStorage.getItem("idUser"),
            detalleVenta: JSON.stringify(productos_envio)
        };
        //console.log(data);
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
                    url: "/addVenta",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Venta guardado con exíto. ", "success");
                        setTimeout(function () { location.href = "/getAllVentasHoy";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function validarVenta() {
    if (cliente == "" || cliente == null) {
        return "Por favor, selecciona a un cliente. ";
    }
    if (productos.length == 0) {
        return "Por favor, selecciona un producto ";;
    }
    return "ok";
}

function detalleVentaAgregar(idV) {
    var data = {
        idVenta: idV
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllVentasById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                venta = data[0];
                //console.log(venta)
                $('#txtNombreClienteVA').text(venta.cliente.idPersona.nombre + ' ' + venta.cliente.idPersona.apellidoP + ' ' + venta.cliente.idPersona.apellidoM);
                $('#txtEmpleadoVA').text(venta.user.nombre + ' ' + venta.user.apellidoP + ' ' + venta.user.apellidoM);
                $('#txtNumeroCelularCVA').text(venta.cliente.idPersona.celular);
                $('#txtFechaVentaVA').text(venta.fecha_venta);
                $('#txtTotalVA').text(venta.total);
                detalleVentaP = venta.detalleVenta;
                $("#tbVentaDetalleVA > tbody").empty();
                for (var i = 0; i < detalleVentaP.length; i++) {
                    $("#tbVentaDetalleVA>tbody").append('<tr><td class="text-center"> <img class="mb-4" src="'+ detalleVentaP[i].producto.img + '" alt="" width="120" height="95"></td><td>' + detalleVentaP[i].producto.modelo + '</td><td>' + detalleVentaP[i].producto.descripcion + '</td><td>' + detalleVentaP[i].cantidad + '</td><td>' + detalleVentaP[i].subtotal + '</td></tr>');
                }
                $('#modalDetalleVentaAgregar').modal('show');
            }
        );

}

function eliminarVentaAgregar(idV) {
    var data = {
        idVenta: idV
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
                url: "/deleteVenta",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Venta eliminada con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllVentasInactivas"; }, 2000)
                }
            );
    });

}

function limpiarModalVentaAgregar() {
    $('#txtNombreClienteVenta').text("-");
    $('#txtCantidadProducto').val(1);
    $('#txtTotalVentaAgregar').text("-");

    cliente = "";
    productos =[]
    productos_envio = []
    llenarTablaDetalleProducto();
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